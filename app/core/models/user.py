from django.contrib.auth.models import AbstractUser
from django.db import models

from .user_manager import UserManager

class CustomUser(AbstractUser):
    full_name = models.CharField(max_length=100, null=True, blank=True)
    phone_number = models.CharField(max_length=20, unique=True, null=True, blank=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)
    conf_password = models.CharField(max_length=100, null=True, blank=True)
    
    objects = UserManager()

