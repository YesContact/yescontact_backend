from django.contrib.auth.models import AbstractUser
from django.db import models

from core.models import Contact
from .user_manager import UserManager

class CustomUser(AbstractUser):
    full_name = models.CharField('İstifadəçinin adı, soyadı', max_length=100)
    phone_number = models.CharField('İstifadəçinin əlaqə nömrəsi', max_length=20, unique=True)
    email = models.EmailField('İstifadəçinin email ünvanı', unique=True)
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE, null=True, blank=True, related_name="user_contacts")
    password = models.CharField('İstifadəçinin parolu', max_length=100)
    password_confirm = models.CharField('İstifadəçinin parolu təsdiqi', max_length=100, null=True, blank=True)
    otp = models.CharField('OTP', max_length=6, null=True, blank=True)
    created_at = models.DateTimeField('İstifadəçinin yaradılma tarixi', auto_now_add=True, null=True, blank=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['password', 'full_name']
    username = models.CharField('İstifadəçinin istifadəçi adı', max_length=100, null=True, blank=True)
    
    objects = UserManager()

    class Meta:
        verbose_name = ('İstifadəçi')
        verbose_name_plural = ('İstifadəçilər')

    def __str__(self) -> str:
        return self.full_name

