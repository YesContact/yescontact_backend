from django.db import models


class Comment(models.Model):
    id = models.AutoField(primary_key=True, unique=True, null=False, blank=False)
    text = models.CharField(max_length=300)

    parent_comment = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        related_name="user_parent_comment",
        blank=True
    )

    user = models.ForeignKey(
        "users.CustomUser",
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        related_name="user_comment",
    )

    survey = models.ForeignKey(
        "survey.Survey",
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        related_name="survey_comment",
    )

    class Meta:
        verbose_name = "Comment"
        verbose_name_plural = "Comments"

    def __str__(self):
        return f'<Comment: {self.id}>'
