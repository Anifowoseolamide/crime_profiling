from django.db import models
from django.conf import settings
from subjects.models import Subject
import uuid

class WantedPerson(models.Model):
    """
    Tracks individuals with active arrest warrants.
    If a subject matches on a field scan and has an active WantedPerson
    record, the officer is immediately alerted.
    """
    PRIORITY_CHOICES = [
        ('ROUTINE', 'Routine'),
        ('URGENT', 'Urgent'),
        ('CRITICAL', 'Critical (Armed & Dangerous)'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='warrants')
    
    warrant_number = models.CharField(max_length=100, unique=True, db_index=True)
    issuing_authority = models.CharField(max_length=200, help_text="e.g. Lagos State High Court")
    reason = models.TextField(help_text="Detailed reason for the warrant")
    
    issued_date = models.DateField()
    expiry_date = models.DateField(null=True, blank=True)
    
    is_active = models.BooleanField(default=True, db_index=True)
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='ROUTINE')
    
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.SET_NULL, 
        null=True,
        related_name='warrants_issued'
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-priority', '-issued_date']
        verbose_name = 'Wanted Person'
        verbose_name_plural = 'Wanted Persons'

    def __str__(self):
        return f"{self.warrant_number} - {self.subject.get_full_name()} ({self.get_priority_display()})"
    
    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super().save(*args, **kwargs)
        
        # When a warrant goes active, auto-update the subject's status
        if self.is_active and self.subject.status != 'WANTED':
            self.subject.status = 'WANTED'
            if self.priority == 'CRITICAL':
                self.subject.is_armed_dangerous = True
            self.subject.save()
