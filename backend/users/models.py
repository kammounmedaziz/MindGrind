from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    """
    Custom User model extending Django's AbstractUser.
    
    Inherits fields: username, first_name, last_name, email, password, 
    is_staff, is_active, date_joined.
    """
    
    # Enforce unique email (standard Django allows duplicates by default)
    email = models.EmailField(unique=True)
    
    # Stores gamification settings, study goals, etc.
    # Example: {"gamification_enabled": True, "study_style": "visual"}
    preferences = models.JSONField(default=dict, blank=True)

    # Timestamps
    updated_at = models.DateTimeField(auto_now=True)

    # We use email as the primary identifier for login instead of username
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    def __str__(self):
        return self.email