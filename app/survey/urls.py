from django.urls import path

from survey.views import (
    SurveyApiView,
    SurveyOptionApiView,
    SurveyCommentApiView,
    SurveyLikeApiView,
    SurveyCommentLikeApiView,
    CreateSurveyApiView,
    # ShowViewCountApiView,
    # ShareSurveyAPIView,
    # SetVoteLimitAPIView,
    SurveyDetailView,
    CreateSurveyOptionApiView,
    SurveyGetViewApi,
    AddSurveyViewApi,
    SurveyCommentCreateAPIView,
    CreateSurveyCommentLikeApiView,
    AddSurveyLikeApiView,
    AddSurveyVoteApi,
    GetSurveyVoteApi,
    ShareSurveyApi,
)

from survey.views import (
    SurveyUserCreateView,
    SurveyUserListView,
    SurveyUserDetailView

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
    path("create-survey-comment/", SurveyCommentCreateAPIView.as_view(), name='create-survey-comment'),

    path("survey-likes/", SurveyLikeApiView.as_view(), name="comment-likes"),
    path("add-survey-like", AddSurveyLikeApiView.as_view(), name='add-survey-like'),

    path("add-comment-like/", CreateSurveyCommentLikeApiView.as_view(), name='add-comment-like'),
    # path("survey-likes/", SurveyLikeApiView.as_view(), name="survey-likes"),
    path(
        "survey-comment-likes/",
        SurveyCommentLikeApiView.as_view(),
        name="survey-comment-likes",
    ),
    # path("show-view-count/", ShowViewCountApiView.as_view(), name="show-view-count"),
    # path("share-survey/", ShareSurveyAPIView.as_view(), name="share-survey"),
    # path("set-vote_limit/", SetVoteLimitAPIView.as_view(), name="set-limit"),

    path('survey/<int:pk>/', SurveyDetailView.as_view(), name='survey-detail'),
    path('create-survey-option/', CreateSurveyOptionApiView.as_view(), name='create-survey-option,'),

    path('get-survey-views/', SurveyGetViewApi.as_view(), name='get-survey-views'),
    path('add-survey-view/', AddSurveyViewApi.as_view(), name='add-survey-view'),

    path('add-survey-vote/', AddSurveyVoteApi.as_view(), name='add-survey-vote'),
    path('get-survey-vote/', GetSurveyVoteApi.as_view(), name='get-survey-vote'),

    path('share-survey/', ShareSurveyApi.as_view(), name='share-survey'),

    path('create-user/', SurveyUserCreateView.as_view(), name='create-user'),
    path('users/', SurveyUserListView.as_view(), name='users'),
    path('user/<int:pk>/', SurveyUserDetailView.as_view(), name='user'),

]
