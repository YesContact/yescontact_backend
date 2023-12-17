from django.db import models


class Like(models.Model):
    id = models.AutoField(primary_key=True, unique=True, null=False, blank=False)

    user = models.ForeignKey(
        "users.CustomUser",
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        related_name="user_like",
    )

    survey = models.ForeignKey(
        "survey.Survey",
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        related_name="survey_like",
    )

    class Meta:
        verbose_name = "Like"
        verbose_name_plural = "Likes"
        unique_together = ('user', 'survey')

    def __str__(self):
        return f'<Like: {self.id}>'
