from django.contrib import admin

from .models import Survey, Comment, Like, CommentLike, SurveyOption, SurveyVote, SurveyView

admin.site.register(Survey)
admin.site.register(Comment)
admin.site.register(Like)
admin.site.register(CommentLike)
admin.site.register(SurveyOption)
admin.site.register(SurveyVote)
admin.site.register(SurveyView)

