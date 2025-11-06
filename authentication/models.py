import uuid
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, Group
from django.db import models
from django.utils import timezone


class UserManager(BaseUserManager):
    """Custom user manager for email-based authentication"""

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email is required')

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True')

        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """Custom user model with UUID primary key and email authentication"""

    # Role choices
    ORGANIZER = 'organizer'
    ATTENDEE = 'attendee'

    ROLE_CHOICES = [
        (ORGANIZER, 'Organizer'),
        (ATTENDEE, 'Attendee'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True, max_length=255)
    firstname = models.CharField(max_length=150)
    lastname = models.CharField(max_length=150)
    role = models.CharField(
        max_length=20, choices=ROLE_CHOICES, default=ATTENDEE)

    # Django required fields
    is_staff = models.BooleanField(default=False)
    date_created = models.DateTimeField(default=timezone.now)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['firstname', 'lastname']

    class Meta:
        db_table = 'users'
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return self.email

    def get_full_name(self):
        return f"{self.firstname} {self.lastname}"

    @property
    def is_organizer(self):
        return self.role == self.ORGANIZER

    @property
    def is_attendee(self):
        return self.role == self.ATTENDEE
