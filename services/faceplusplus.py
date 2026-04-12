import logging
import requests
from django.conf import settings

logger = logging.getLogger(__name__)

class FacePPError(Exception):
    """Raised when Face++ returns a non-200 response or an error in JSON."""
    pass

class FacePlusPlusClient:
    def __init__(self):
        self.api_key = settings.FACEPP_API_KEY
        self.api_secret = settings.FACEPP_API_SECRET
        self.region = settings.FACEPP_REGION or 'api-us'
        self.base_url = f"https://{self.region}.faceplusplus.com/facepp/v3"
        self.outer_id = settings.FACEPP_OUTER_ID or 'lagoscp_faceset'
        self.threshold = settings.FACEPP_THRESHOLD or 80
        
        self.mock_mode = not self.api_key or "your-api-key" in self.api_key

        if self.mock_mode:
            logger.warning(
                'Face++ MOCK MODE enabled — no real face recognition. '
                'Set FACEPP_API_KEY in .env to enable live recognition.'
            )

    def _get_common_params(self):
        return {
            'api_key': self.api_key,
            'api_secret': self.api_secret,
        }

    def _post(self, endpoint, data=None, files=None):
        url = f"{self.base_url}/{endpoint}"
        params = self._get_common_params()
        
        try:
            response = requests.post(
                url,
                data={**params, **(data or {})},
                files=files,
                timeout=30
            )
            res_json = response.json()
            if 'error_message' in res_json:
                raise FacePPError(f"Face++ Error: {res_json['error_message']}")
            response.raise_for_status()
            return res_json
        except requests.exceptions.RequestException as exc:
            raise FacePPError(f"Face++ connection error: {exc}") from exc

    def ensure_faceset_exists(self):
        """Creates the Faceset if it doesn't exist."""
        if self.mock_mode:
            return
        
        try:
            self._post('faceset/create', data={'outer_id': self.outer_id})
            logger.info(f"Created Face++ Faceset: {self.outer_id}")
        except FacePPError as e:
            if "OUTER_ID_EXIST" in str(e) or "FACESET_EXIST" in str(e):
                pass # Already exists
            else:
                raise e

    def _detect(self, image_bytes):
        """Detect faces and return face_tokens."""
        res = self._post(
            'detect',
            files={'image_file': ('image.jpg', image_bytes, 'image/jpeg')}
        )
        faces = res.get('faces', [])
        if not faces:
            return []
        return [f['face_token'] for f in faces]

    def enrol_subject(self, subject_id, image_bytes):
        """
        Detect, set user_id, and add to Faceset in one flow.
        """
        if self.mock_mode:
            return {'face_token': 'mock_token', 'user_id': subject_id}

        # 1. Detect
        tokens = self._detect(image_bytes)
        if not tokens:
            raise FacePPError("No face detected in the image.")
        
        face_token = tokens[0] # Take the first/primary face

        # 2. Set User ID
        self._post('face/setuserid', data={
            'face_token': face_token,
            'user_id': subject_id
        })

        # 3. Add to Faceset
        self.ensure_faceset_exists()
        self._post('faceset/addface', data={
            'outer_id': self.outer_id,
            'face_tokens': face_token
        })

        return {'face_token': face_token, 'user_id': subject_id}

    def identify(self, image_bytes):
        """
        Search for a face in the Faceset.
        """
        if self.mock_mode:
            return {
                'match_found': False,
                'subject_id': None,
                'confidence': 0.0,
                'raw': {'_mock': True}
            }

        # 3. Search for a face in the Faceset
        self.ensure_faceset_exists()
        res = self._post(
            'search',
            data={'outer_id': self.outer_id},
            files={'image_file': ('search.jpg', image_bytes, 'image/jpeg')}
        )

        results = res.get('results', [])
        if not results:
            return {
                'match_found': False,
                'subject_id': None,
                'confidence': 0.0,
                'raw': res
            }

        best_match = results[0]
        confidence = best_match.get('confidence', 0.0)
        user_id = best_match.get('user_id')

        match_found = confidence >= self.threshold

        return {
            'match_found': match_found,
            'subject_id': user_id if match_found else None,
            'confidence': confidence,
            'raw': res
        }

    def delete_subject(self, subject_id):
        """
        Face++ doesn't easily allow deleting by user_id without knowing face_tokens.
        We'll treat this as a no-op or a log for now, as we don't store face_tokens.
        In a real production system, you'd store tokens in a mapping table to delete them.
        """
        if self.mock_mode:
            logger.info(f"[MOCK] Deleting subject {subject_id}")
            return

        logger.warning(
            f"Face++ delete_subject called for {subject_id}. "
            "Individual face token deletion not implemented as tokens are not persisted."
        )

# Singleton instance
faceplusplus = FacePlusPlusClient()
