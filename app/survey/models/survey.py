import secrets
from datetime import datetime

import pytz
from django.db import models
from django.utils import timezone


def generate_custom_token():
    return secrets.token_urlsafe(100)


class Survey(models.Model):
    id = models.AutoField(primary_key=True, unique=True, null=False, blank=False)
    survey_id = models.CharField(unique=True, default=generate_custom_token, max_length=500)

    title = models.CharField(max_length=300, null=False)
    description = models.CharField(max_length=1000, null=False)

    paid = models.BooleanField(default=False)
    active = models.BooleanField(default=False)

    vote_limit = models.IntegerField(default=0)
    view_count = models.IntegerField(default=0)

    start_time = models.DateTimeField(default=timezone.now)
    end_time = models.DateTimeField()

    user = models.ForeignKey(
        "users.CustomUser",
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        related_name="user_surveys",
    )

    cost = models.IntegerField(null=False)


    class Meta:
        verbose_name = "Survey"
        verbose_name_plural = "Surveys"

    def __str__(self):
        return f'<Survey {self.title}>'

    def update_start_time(self):
        self.start_time = timezone.now()

    def check_date_difference(self, end_time):
        date_object = datetime.strptime(end_time, '%Y-%m-%dT%H:%M:%S.%fZ').replace(tzinfo=pytz.UTC)
        return date_object >= self.start_time

