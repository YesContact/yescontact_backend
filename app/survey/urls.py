from django.urls import path

from survey.views import (
    SurveyApiView,
    SurveyOptionApiView,
    SurveyCommentApiView,
    SurveyLikeApiView,
    SurveyCommentLikeApiView,
    CreateFreeSurveyApiView,
    CreatePaidSurveyApiView,
    # ShowViewCountApiView,
    # ShareSurveyAPIView,
    # SetVoteLimitAPIView,
    SurveyDetailView,
    CreateSurveyOptionApiView,
    SurveyOptionDetailView,
    SurveyGetViewApi,
    AddSurveyViewApi,
    SurveyCommentCreateAPIView,
    CreateSurveyCommentLikeApiView,
    AddSurveyLikeApiView,
    AddSurveyVoteApi,
    GetSurveyVoteApi,
    ShareSurveyApi, JetonConverterView, StartSurveyApiView, WalletIncreaseView,
    SurveyCommentDetailView
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
        "create-free-survey/",
        CreateFreeSurveyApiView.as_view(),
        name="create-survey",
    ),
    path(
        "create-paid-survey/",
        CreatePaidSurveyApiView.as_view(),
        name="create-survey",
    ),
    path("survey-comments/", SurveyCommentApiView.as_view(), name="survey-comments"),
    path("create-survey-comment/", SurveyCommentCreateAPIView.as_view(), name='create-survey-comment'),
    path("survey-comment/<int:pk>", SurveyCommentDetailView.as_view(), name='survey-comment'),

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

    path('survey-option/<int:pk>/', SurveyOptionDetailView.as_view(), name='survey-option-detail'),

    path('get-survey-views/', SurveyGetViewApi.as_view(), name='get-survey-views'),
    path('add-survey-view/', AddSurveyViewApi.as_view(), name='add-survey-view'),

    path('add-survey-vote/', AddSurveyVoteApi.as_view(), name='add-survey-vote'),
    path('get-survey-vote/', GetSurveyVoteApi.as_view(), name='get-survey-vote'),

    path('share-survey/', ShareSurveyApi.as_view(), name='share-survey'),

    path('create-user/', SurveyUserCreateView.as_view(), name='create-user'),
    path('users/', SurveyUserListView.as_view(), name='users'),
    path('user/<int:pk>/', SurveyUserDetailView.as_view(), name='user'),

    path('convert-to-jeton', JetonConverterView.as_view(), name='convert-jeton'),

    # path('start-survey/', StartSurveyApiView.as_view(), name='start-survey'),

    path('increase-wallet', WalletIncreaseView.as_view(), name='increase-wallet'),

]
