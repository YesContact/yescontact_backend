from celery import shared_task

from time import sleep


@shared_task(bind=True)
def process_survey_start_time(seconds):
    sleep(seconds)
    return seconds

@shared_task(bind=True)
def process_survey_end_time(seconds):
    sleep(seconds)
    return seconds
