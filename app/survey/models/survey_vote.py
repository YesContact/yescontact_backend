from django.db import models


class SurveyVote(models.Model):
    id = models.AutoField(primary_key=True, unique=True, null=False, blank=False)

    survey_option = models.ForeignKey(
        "survey.SurveyOption",
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        related_name="vote_survey_option",
    )

    survey = models.ForeignKey(
        "survey.Survey",
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        related_name="vote_survey"
    )

    user = models.ForeignKey(
        "users.CustomUser",
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        related_name="vote_user",
    )

    amount = models.IntegerField(null=False, default=0)

    class Meta:
        verbose_name = "SurveyVote"
        verbose_name_plural = "SurveyVotes"
        unique_together = ('survey_option', 'user')

    def __str__(self):
        return f'<SurveyVote: {self.id}>'


