from django.urls import path

from survey.views import (
    SurveyApiView,
    SurveyOptionApiView,
    SurveyCommentApiView,
    SurveyLikeApiView,
    SurveyCommentLikeApiView,
    CreateSurveyApiView,
    ShowViewCountApiView,
    ShareSurveyAPIView,
    SetVoteLimitAPIView,
)

urlpatterns = [
    path("surveys/", SurveyApiView.as_view(), name="surveys"),
    path("survey-options/", SurveyOptionApiView.as_view(), name="survey-options"),
    path(
        "create-survey/",
        CreateSurveyApiView.as_view(),
        name="create-survey-option",
    ),
    path("survey-comments/", SurveyCommentApiView.as_view(), name="survey-comments"),
    path("survey-likes/", SurveyLikeApiView.as_view(), name="survey-likes"),
    path(
        "survey-comment-likes/",
        SurveyCommentLikeApiView.as_view(),
        name="survey-comment-likes",
    ),
    path("show-view-count/", ShowViewCountApiView.as_view(), name="show-view-count"),
    path("share-survey/", ShareSurveyAPIView.as_view(), name="share-survey"),
    path("set-vote_limit/", SetVoteLimitAPIView.as_view(), name="set-limit"),
]
