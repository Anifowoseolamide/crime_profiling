"""
CompreFace REST API client for LagosCP.

Wraps the three operations needed:
  - enrol_subject()   → add a mugshot to CompreFace recognition collection
  - identify()        → match a field photo against enrolled faces
  - delete_subject()  → remove all faces for a subject (record expungement)

MOCK MODE
---------
If settings.COMPREFACE_URL is empty, the client returns realistic mock
responses so development and testing can proceed without a running
CompreFace instance.
"""

import logging
import uuid
import requests
from django.conf import settings

logger = logging.getLogger(__name__)


class CompreFaceError(Exception):
    """Raised when CompreFace returns a non-2xx response."""
    pass


class CompreFaceClient:
    def __init__(self):
        self.base_url = settings.COMPREFACE_URL.rstrip('/')
        self.api_key = settings.COMPREFACE_API_KEY
        self.threshold = settings.COMPREFACE_THRESHOLD
        self.det_prob_threshold = settings.COMPREFACE_DET_PROB_THRESHOLD
        self.mock_mode = not bool(self.base_url)

        if self.mock_mode:
            logger.warning(
                'CompreFace MOCK MODE enabled — no real face recognition. '
                'Set COMPREFACE_URL in .env to enable live recognition.'
            )

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _headers(self):
        return {'x-api-key': self.api_key}

    def _post(self, path, files, params=None):
        url = f"{self.base_url}{path}"
        try:
            response = requests.post(
                url,
                params=params or {},
                headers=self._headers(),
                files=files,
                timeout=30,
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as exc:
            body = exc.response.text if exc.response is not None else ''
            raise CompreFaceError(f"CompreFace HTTP {exc.response.status_code}: {body}") from exc
        except requests.exceptions.RequestException as exc:
            raise CompreFaceError(f"CompreFace connection error: {exc}") from exc

    def _delete(self, path, params=None):
        url = f"{self.base_url}{path}"
        try:
            response = requests.delete(
                url,
                params=params or {},
                headers=self._headers(),
                timeout=15,
            )
            response.raise_for_status()
        except requests.exceptions.RequestException as exc:
            raise CompreFaceError(f"CompreFace delete error: {exc}") from exc

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def enrol_subject(self, subject_id: str, image_bytes: bytes) -> dict:
        """
        Enrol a mugshot under subject_id in the CompreFace recognition collection.

        Returns CompreFace response dict:
          { "image_id": "...", "subject": "lagoscp-<uuid>" }
        """
        if self.mock_mode:
            return {
                'image_id': str(uuid.uuid4()),
                'subject': subject_id,
                '_mock': True,
            }

        return self._post(
            '/api/v1/recognition/faces',
            params={'subject': subject_id},
            files={'file': ('mugshot.jpg', image_bytes, 'image/jpeg')},
        )

    def identify(self, image_bytes: bytes, limit: int = 1) -> dict:
        """
        Match a field photo against all enrolled faces.

        Returns a normalised dict:
        {
            "match_found": bool,
            "subject_id": str | None,       # compreface subject_id
            "confidence": float | None,     # 0.0 – 1.0
            "raw": dict                     # full CompreFace response
        }
        """
        if self.mock_mode:
            # Return a mock "no match" so field scan works out of the box.
            # Change to mock_match=True in tests if you need a positive result.
            return {
                'match_found': False,
                'subject_id': None,
                'confidence': None,
                'raw': {'_mock': True, 'result': []},
            }

        raw = self._post(
            '/api/v1/recognition/recognize',
            params={
                'limit': limit,
                'det_prob_threshold': self.det_prob_threshold,
            },
            files={'file': ('field_photo.jpg', image_bytes, 'image/jpeg')},
        )

        return self._parse_identify_response(raw)

    def _parse_identify_response(self, raw: dict) -> dict:
        """Extract the best match from CompreFace recognition response."""
        try:
            results = raw.get('result', [])
            if not results:
                return {'match_found': False, 'subject_id': None, 'confidence': None, 'raw': raw}

            # CompreFace returns per-detected-face results
            best_match = None
            best_score = 0.0

            for face_result in results:
                subjects = face_result.get('subjects', [])
                for subject in subjects:
                    score = subject.get('similarity', 0.0)
                    if score > best_score:
                        best_score = score
                        best_match = subject.get('subject')

            if best_match and best_score >= self.threshold:
                return {
                    'match_found': True,
                    'subject_id': best_match,
                    'confidence': round(best_score, 4),
                    'raw': raw,
                }
            return {'match_found': False, 'subject_id': None, 'confidence': round(best_score, 4), 'raw': raw}

        except (KeyError, IndexError, TypeError) as exc:
            logger.error('Failed to parse CompreFace response: %s — raw: %s', exc, raw)
            return {'match_found': False, 'subject_id': None, 'confidence': None, 'raw': raw}

    def delete_subject(self, subject_id: str) -> None:
        """
        Remove all enrolled faces for a subject (e.g. record expungement).
        Safe to call even if subject has no enrolled faces.
        """
        if self.mock_mode:
            logger.info('[MOCK] delete_subject called for %s', subject_id)
            return

        try:
            self._delete('/api/v1/recognition/faces', params={'subject': subject_id})
        except CompreFaceError as exc:
            # Log but do not propagate — subject may never have been enrolled
            logger.warning('delete_subject for %s failed (may not exist): %s', subject_id, exc)


# Module-level singleton — import and use directly
compreface = CompreFaceClient()
