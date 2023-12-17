from django.urls import path

from survey.views import SurveyApiView

urlpatterns = [
    path("surveys/", SurveyApiView.as_view(), name="surveys"),
]
