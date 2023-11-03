from django.db import models
from app.utils.base_model import BaseModel

class Contact(BaseModel):
    first_name = models.CharField(max_length=100, null=True, blank=True)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    phone_number = models.CharField(max_length=20, unique=True, null=True, blank=True)

    class Meta:
        verbose_name = 'Contact'
        verbose_name_plural = 'Contacts'

    def __str__(self):
        return self.phone_number
