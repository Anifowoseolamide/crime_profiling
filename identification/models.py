from django.db import models
from django.conf import settings
from subjects.models import Subject
import uuid

class IdentificationLog(models.Model):
    """
    Log of an officer capturing a photo in the field and running it 
    against the CompreFace biometric database.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    officer = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.SET_NULL, 
        null=True,
        related_name='identifications_performed'
    )
    
    # Null if CompreFace returns no match
    subject = models.ForeignKey(
        Subject, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='identification_logs'
    )
    
    # The actual photo taken by the officer
    field_image_url = models.URLField(max_length=500)
    
    # Face++ results
    match_found = models.BooleanField(default=False)
    confidence_score = models.FloatField(null=True, blank=True)
    face_recognition_response = models.JSONField(blank=True, null=True, help_text="Raw API response")
    
    # Context
    location = models.CharField(max_length=255, blank=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    notes = models.TextField(blank=True)
    device_id = models.CharField(max_length=100, blank=True)
    
    timestamp = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['officer', 'timestamp']),
            models.Index(fields=['subject', 'timestamp']),
            models.Index(fields=['match_found']),
        ]

    def __str__(self):
        match_str = f"Matched: {self.subject.get_full_name()}" if self.match_found else "No Match"
        return f"Scan by {self.officer.badge_number} at {self.timestamp.strftime('%H:%M')} - {match_str}"
