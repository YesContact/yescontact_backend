from django.db import models


class SurveyView(models.Model):
    id = models.AutoField(primary_key=True, unique=True, null=False, blank=False)

    survey = models.ForeignKey(
        "survey.Survey",
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        related_name="view_survey",
    )

    user = models.ForeignKey(
        "users.CustomUser",
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        related_name="view_user",
    )
