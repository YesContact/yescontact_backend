from django.db import models


class SurveyOption(models.Model):
    id = models.AutoField(primary_key=True, unique=True, null=False, blank=False)

    title = models.CharField(max_length=100, null=False, blank=False)

    image_file = models.FileField(upload_to='uploads/')
    # image_path = models.FilePathField(path='uploads/')

    # options = models.IntegerField(default=2)

    survey = models.ForeignKey(
        "survey.Survey",
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        related_name="survey_option",
    )

    class Meta:
        verbose_name = "SurveyOption"
        verbose_name_plural = "SurveyOptions"

    def __str__(self):
        return f'<SurveyOption: {self.id}>'
