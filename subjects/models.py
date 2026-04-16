from django.db import models
from django.conf import settings
import uuid


class Subject(models.Model):
    """
    Core Criminal Profile model for LagosCP.
    """
    GENDER_CHOICES = [
        ('MALE', 'Male'),
        ('FEMALE', 'Female'),
        ('OTHER', 'Other'),
    ]

    RISK_LEVEL_CHOICES = [
        ('LOW', 'Low Risk'),
        ('MEDIUM', 'Medium Risk'),
        ('HIGH', 'High Risk'),
        ('EXTREME', 'Extreme Risk'),
    ]

    STATUS_CHOICES = [
        ('ACTIVE', 'Active on Streets'),
        ('WANTED', 'Wanted'),
        ('INCARCERATED', 'Incarcerated'),
        ('DECEASED', 'Deceased'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    # Personal Details
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    aliases = models.JSONField(default=list, blank=True, help_text='List of known a.k.a.')
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=20, choices=GENDER_CHOICES, default='MALE')
    
    # Demographic / Location
    nationality = models.CharField(max_length=100, default='Nigerian')
    state_of_origin = models.CharField(max_length=100, blank=True)
    lga_of_origin = models.CharField(max_length=100, blank=True)
    address = models.TextField(blank=True)
    phone_numbers = models.JSONField(default=list, blank=True)
    
    # physical Profile
    identifying_marks = models.TextField(blank=True, help_text='Scars, tattoos, clear features')
    
    # Geographic Tracking
    last_known_location = models.CharField(max_length=255, blank=True)
    last_known_lat = models.FloatField(null=True, blank=True)
    last_known_lng = models.FloatField(null=True, blank=True)
    last_seen_date = models.DateTimeField(null=True, blank=True)    
    # Assessment
    risk_level = models.CharField(max_length=20, choices=RISK_LEVEL_CHOICES, default='LOW')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ACTIVE')
    is_armed_dangerous = models.BooleanField(default=False)
    
    # Integration
    face_recognition_id = models.CharField(max_length=100, unique=True, blank=True, null=True)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['last_name', 'first_name']
        verbose_name = 'Subject'
        verbose_name_plural = 'Subjects'
        indexes = [
            models.Index(fields=['last_name', 'first_name']),
            models.Index(fields=['face_recognition_id']),
            models.Index(fields=['status']),
            models.Index(fields=['risk_level']),
        ]

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.get_status_display()})"
    
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    @property
    def primary_mugshot(self):
        primary = self.mugshots.filter(is_primary=True).first()
        if primary:
            return primary.image_url
        latest = self.mugshots.order_by('-capture_date').first()
        return latest.image_url if latest else None
    
    def save(self, *args, **kwargs):
        # Auto-generate Face Recognition ID if missing
        if not self.face_recognition_id:
            self.face_recognition_id = f"lagoscp_{self.id.hex}"
        super().save(*args, **kwargs)


class Mugshot(models.Model):
    """
    Photographic records for a subject. Multiple variants (angles/ages) 
    can be enrolled in CompreFace to improve recognition.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='mugshots')
    
    # Store the Cloudinary or S3 URL
    image_url = models.URLField()
    is_primary = models.BooleanField(default=False)
    
    # Geographic Context
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    
    capture_date = models.DateTimeField(auto_now_add=True)
    captured_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.SET_NULL, 
        null=True,
        blank=True
    )
    
    enrolled_in_face_recognition = models.BooleanField(default=False)

    class Meta:
        ordering = ['-capture_date']

    def __str__(self):
        return f"Mugshot for {self.subject.get_full_name()} ({self.capture_date.date()})"
    
    def save(self, *args, **kwargs):
        # Only one primary mugshot per subject
        if self.is_primary:
            Mugshot.objects.filter(subject=self.subject, is_primary=True).update(is_primary=False)
        super().save(*args, **kwargs)
