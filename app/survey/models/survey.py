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
    image = models.ImageField(upload_to='uploads/surveys/', null=False, default='uploads/surveys/default.png')

    paid = models.BooleanField(default=False)
    payment = models.BooleanField(default=False)
    active = models.BooleanField(default=False)
    status = models.CharField(max_length=100, default="ready_to_start", choices=[
        ("ready_to_start", "Ready to start"),
        ("active", "Active"),
        ("expired", "Expired"),
        ("aborted", "Aborted"),
    ])

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
    created_at = models.DateTimeField(auto_now_add=True)
    visibility = models.CharField(max_length=100, default="public", choices=[
        ("public", "Public"),
        ("contact", "Contact"),
    ])


    class Meta:
        verbose_name = "Survey"
        verbose_name_plural = "Surveys"

    def __str__(self):
        return f'<Survey {self.title}>'

    def update_start_time(self):
        self.start_time = timezone.now()

    def check_date_difference(self, end_time):
        if isinstance(end_time, datetime):
            return end_time >= self.start_time
        elif isinstance(end_time, str):
            date_object = datetime.strptime(end_time, '%Y-%m-%dT%H:%M:%S.%fZ').replace(tzinfo=pytz.UTC)
            return date_object >= self.start_time

    def seconds_until_start(self):
        return int((self.start_time - timezone.now()).total_seconds())
    
    def seconds_until_end(self):
        return int((self.end_time - timezone.now()).total_seconds())


class CompletedSurvey(models.Model):
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE)
    completed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Completed Survey"
        verbose_name_plural = "Completed Surveys"
