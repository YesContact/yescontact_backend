from django.urls import path

from core.views import *
from core.apis import *
from core.serializers import *
from users.apis import *
from rest_framework.routers import DefaultRouter


from django.urls import path, include
from core.views import chatPage
from django.contrib.auth.views import LoginView, LogoutView
 
 
urlpatterns = [
    path("", chatPage, name="chat-page"),
 
    # login-section
    path("auth/login/", LoginView.as_view
         (template_name="chat/LoginPage.html"), name="login-user"),
    path("auth/logout/", LogoutView.as_view(), name="logout-user"),
]