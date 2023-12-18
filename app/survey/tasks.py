from celery import shared_task
from datetime import timedelta
from django.utils import timezone
from .models import Survey

@shared_task
def expire_survey(survey_id):
    try:
        survey = Survey.objects.get(id=survey_id)
        survey_deadline = survey.end_time

        if survey_deadline and survey_deadline < timezone.now():
            survey.is_expired = True
            survey.delete()

    except Survey.DoesNotExist:
        raise Exception(f"Survey with ID {survey_id} does not exist.")