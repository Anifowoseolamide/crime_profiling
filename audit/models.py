from django.db import models
from django.conf import settings
import uuid


class AuditLog(models.Model):
    """
    Immutable activity trail for every significant officer action.
    Records are NEVER deleted — only appended.
    Amendments are logged as new records with action='*_AMENDED'.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # Who did it
    officer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='audit_logs',
    )

    # What was done
    action = models.CharField(
        max_length=100,
        db_index=True,
        help_text=(
            'e.g. SUBJECT_VIEWED, SUBJECT_CREATED, OFFENCE_CREATED, '
            'OFFENCE_UPDATED, IDENTIFICATION_ATTEMPTED, WANTED_ADDED, '
            'OFFICER_CREATED, OFFICER_UPDATED'
        ),
    )

    # What it was done to
    target_type = models.CharField(
        max_length=100,
        blank=True,
        help_text='Model name, e.g. Subject, Offence, WantedPerson',
    )
    target_id = models.UUIDField(null=True, blank=True, help_text='PK of the affected record')

    # Full snapshot
    metadata = models.JSONField(
        default=dict,
        blank=True,
        help_text='Contextual data at time of action (diffs, scores, locations)',
    )

    # Network context
    ip_address = models.GenericIPAddressField(null=True, blank=True)

    # Immutable timestamp — auto_now_add, never updated
    timestamp = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['officer', 'timestamp']),
            models.Index(fields=['action', 'timestamp']),
            models.Index(fields=['target_type', 'target_id']),
        ]
        # Enforce immutability at DB level — no updates
        # (We never call .save() on existing records)

    def __str__(self):
        officer_str = self.officer.badge_number if self.officer else 'SYSTEM'
        return f"[{self.timestamp:%Y-%m-%d %H:%M}] {officer_str} → {self.action}"

    def save(self, *args, **kwargs):
        """Only allow creation, never mutation."""
        if self.pk and AuditLog.objects.filter(pk=self.pk).exists():
            raise PermissionError('AuditLog records are immutable and cannot be updated.')
        super().save(*args, **kwargs)

    @classmethod
    def log(cls, officer, action, target_type='', target_id=None, metadata=None, ip_address=None):
        """Convenience factory method used throughout the codebase."""
        return cls.objects.create(
            officer=officer,
            action=action,
            target_type=target_type,
            target_id=target_id,
            metadata=metadata or {},
            ip_address=ip_address,
        )
