from django.db import models
from django.conf import settings
from subjects.models import Subject
from authentication.models import PoliceStation
from django.utils import timezone
import uuid

class Offence(models.Model):
    """
    Log of a criminal offence committed by a Subject.
    Includes auto-generating an offence_code based on the incident date.
    """
    CATEGORY_CHOICES = [
        ('THEFT', 'Theft'),
        ('ASSAULT', 'Assault / Battery'),
        ('ARMED_ROBBERY', 'Armed Robbery'),
        ('FRAUD', 'Fraud / Scam'),
        ('HOMICIDE', 'Homicide / Murder'),
        ('KIDNAPPING', 'Kidnapping'),
        ('EXTORTION', 'Extortion'),
        ('DRUGS', 'Drug Trafficking / Possession'),
        ('CYBERCRIME', 'Cybercrime'),
        ('TRAFFIC', 'Traffic Violation'),
        ('OTHER', 'Other'),
    ]

    SEVERITY_CHOICES = [
        ('MINOR', 'Minor'),
        ('MODERATE', 'Moderate'),
        ('SERIOUS', 'Serious'),
        ('VIOLENT', 'Violent'),
        ('CAPITAL', 'Capital Offence'),
    ]

    STATUS_CHOICES = [
        ('OPEN', 'Open'),
        ('UNDER_INVESTIGATION', 'Under Investigation'),
        ('RESOLVED', 'Resolved'),
        ('ACQUITTED', 'Acquitted'),
        ('DISMISSED', 'Dismissed'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    # E.g. LG-ARB-2025-00184
    offence_code = models.CharField(max_length=50, unique=True, db_index=True)
    
    subject = models.ForeignKey(Subject, on_delete=models.RESTRICT, related_name='offences')
    
    # Classification
    offence_category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    severity = models.CharField(max_length=20, choices=SEVERITY_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='OPEN')
    
    # Details
    offence_title = models.CharField(max_length=200, help_text="Short descriptor, e.g. 'Robbery at gunpoint'")
    description = models.TextField()
    
    # Timing
    incident_date = models.DateTimeField(help_text="When the offence occurred")
    reported_date = models.DateTimeField(auto_now_add=True, help_text="When logged in system")
    
    # Geography
    location = models.CharField(max_length=255)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    
    # Law Enforcement
    arresting_officer = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.SET_NULL, 
        null=True,
        related_name='arrests_made'
    )
    station = models.ForeignKey(PoliceStation, on_delete=models.RESTRICT, related_name='offences_handled')
    
    # Evidence & Outcome
    evidence_images = models.JSONField(default=list, blank=True, help_text="List of Cloudinary URLs")
    court_case_number = models.CharField(max_length=100, blank=True, null=True)
    penalty_issued = models.TextField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-incident_date']
        indexes = [
            models.Index(fields=['offence_code']),
            models.Index(fields=['subject', 'status']),
            models.Index(fields=['offence_category']),
        ]

    def __str__(self):
        return f"{self.offence_code} - {self.subject.get_full_name()}"

    def save(self, *args, **kwargs):
        if not self.offence_code:
            self.offence_code = self._generate_offence_code()
        super().save(*args, **kwargs)

    def _generate_offence_code(self):
        """
        Format: LG-{CAT}-{YEAR}-{SEQ}
        Example: LG-ARB-2025-00184
        Uses the incident_date's year.
        """
        # Determine 3-letter category code
        cat_codes = {
            'THEFT': 'TFT', 'ASSAULT': 'ASS', 'ARMED_ROBBERY': 'ARB',
            'FRAUD': 'FRD', 'HOMICIDE': 'HOM', 'KIDNAPPING': 'KID',
            'EXTORTION': 'EXT', 'DRUGS': 'DRG', 'CYBERCRIME': 'CYB',
            'TRAFFIC': 'TRF', 'OTHER': 'OTH'
        }
        cat_code = cat_codes.get(self.offence_category, 'OTH')
        
        # Use incident_date year
        # Note: if incident_date isn't set yet (e.g. before first save), we default to now.
        year = self.incident_date.year if self.incident_date else timezone.now().year
        
        # Determine sequence number for this category and year
        # Find the max sequence number currently in the DB
        prefix = f"LG-{cat_code}-{year}-"
        last_offence = Offence.objects.filter(offence_code__startswith=prefix).order_by('-offence_code').first()
        
        if last_offence:
            # Extract sequence number from e.g. 'LG-ARB-2025-00184'
            try:
                last_seq = int(last_offence.offence_code.split('-')[-1])
                new_seq = last_seq + 1
            except ValueError:
                new_seq = 1
        else:
            new_seq = 1
            
        return f"{prefix}{new_seq:05d}"
