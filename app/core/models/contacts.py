from django.db import models
from app.utils.base_model import BaseModel


class Contact(BaseModel):
    full_name = models.CharField(max_length=100, null=True, blank=True)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    user = models.ForeignKey(
        "users.CustomUser",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="user_contacts",
    )

    class Meta:
        verbose_name = "Contact"
        verbose_name_plural = "Contacts"

    def __str__(self):
        if self.phone_number:
            return f"{self.full_name} ({self.phone_number})"
        else:
            return f"{self.full_name} (No phone number)"


# nomreninsahibi ??
