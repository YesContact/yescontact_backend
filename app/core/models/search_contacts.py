from django.db import models


class SearchContacts(models.Model):
    phone_number = models.CharField(max_length=20, unique=True, null=True, blank=True)
    searching_date = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    user = models.ForeignKey(
        "users.CustomUser",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="user_search_contacts",
    )
