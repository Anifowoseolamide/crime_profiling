from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone
import uuid


class PoliceStation(models.Model):
    """
    Lagos State Police Command station / division.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    division = models.CharField(max_length=200, blank=True)
    lga = models.CharField(max_length=100, verbose_name='LGA')
    address = models.TextField(blank=True)
    phone = models.CharField(max_length=30, blank=True)

    # Commanding officer set via signal / post-save to avoid circular FK
    commanding_officer = models.ForeignKey(
        'authentication.Officer',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='commanded_stations',
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']
        verbose_name = 'Police Station'
        verbose_name_plural = 'Police Stations'

    def __str__(self):
        return f"{self.name} — {self.lga}"


class OfficerManager(BaseUserManager):
    def create_user(self, badge_number, password=None, **extra_fields):
        if not badge_number:
            raise ValueError('Badge number is required')
        user = self.model(badge_number=badge_number.upper().strip(), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, badge_number, password=None, **extra_fields):
        extra_fields.setdefault('role', 'ADMIN')
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('rank', 'Commissioner of Police')
        return self.create_user(badge_number, password, **extra_fields)


class Officer(AbstractBaseUser, PermissionsMixin):
    """
    Custom user model for Lagos State Police officers.
    Authentication is via badge_number + password (not username/email).
    """
    ROLE_CHOICES = [
        ('FIELD_OFFICER', 'Field Officer'),
        ('SUPERVISOR', 'Supervisor'),
        ('ANALYST', 'Analyst'),
        ('ADMIN', 'Administrator'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # Primary identifier (replaces username)
    badge_number = models.CharField(
        max_length=50,
        unique=True,
        db_index=True,
        help_text='e.g. LSP-04821',
    )

    # Personal details
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=30, blank=True)

    # Role & station
    rank = models.CharField(max_length=100, help_text='e.g. Inspector, Sergeant')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='FIELD_OFFICER')
    station = models.ForeignKey(
        PoliceStation,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='officers',
    )

    # Django auth internals
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    # Timestamps
    last_login = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = OfficerManager()

    USERNAME_FIELD = 'badge_number'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'rank']

    class Meta:
        ordering = ['badge_number']
        verbose_name = 'Officer'
        verbose_name_plural = 'Officers'

    def __str__(self):
        return f"{self.badge_number} — {self.rank} {self.get_full_name()}"

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}".strip()

    @property
    def is_admin(self):
        return self.role == 'ADMIN'

    @property
    def is_supervisor(self):
        return self.role in ('SUPERVISOR', 'ADMIN')

    @property
    def is_field_officer(self):
        return self.role == 'FIELD_OFFICER'

    @property
    def station_name(self):
        return self.station.name if self.station else 'Unassigned'
