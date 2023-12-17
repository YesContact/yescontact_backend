from django.urls import path

from survey.views import SurveyApiView, SurveyOptionApiView, SurveyCommentApiView, SurveyLikeApiView

urlpatterns = [
    path("surveys/", SurveyApiView.as_view(), name="surveys"),
    path("survey-options/", SurveyOptionApiView.as_view(), name="survey-options"),
    path("survey-comments/", SurveyCommentApiView.as_view(), name="survey-comments"),
    path("survey-likes/", SurveyLikeApiView.as_view(), name="survey-likes")
]
