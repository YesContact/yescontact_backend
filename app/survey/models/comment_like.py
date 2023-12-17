from django.db import models


class CommentLike(models.Model):
    id = models.AutoField(primary_key=True, unique=True, null=False, blank=False)

    user = models.ForeignKey(
        "users.CustomUser",
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        related_name="user_comment_like",
    )

    comment = models.ForeignKey(
        'survey.Comment',
        on_delete=models.CASCADE,
        null=True,
        related_name="comment_like"
    )

    class Meta:
        verbose_name = "CommentLike"
        verbose_name_plural = "CommentLikes"
        unique_together = ('user', 'comment')

    def __str__(self):
        return f'<CommentLike: {self.id}>'
