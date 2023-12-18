import secrets

from django.db import models


def generate_custom_token():
    return secrets.token_urlsafe(100)


class Survey(models.Model):
    id = models.AutoField(primary_key=True, unique=True, null=False, blank=False)
    survey_id = models.TextField(unique=True, default=generate_custom_token)

    title = models.CharField(max_length=300, null=False)
    description = models.CharField(max_length=1000, null=False)

    paid = models.BooleanField(default=False)
    active = models.BooleanField(default=False)

    vote_limit = models.IntegerField(default=0)
    view_count = models.IntegerField(default=0)

    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    user = models.ForeignKey(
        "users.CustomUser",
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        related_name="user_surveys",
    )

    class Meta:
        verbose_name = "Survey"
        verbose_name_plural = "Surveys"

    def __str__(self):
        return f'<Survey {self.title}>'






