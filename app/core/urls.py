from django.urls import path, include
from django.contrib.auth import views as auth_views

from .views import *
from .apis import *
from .serializers import *

urlpatterns = [
    path('login', login, name='login'),
    path('logout', auth_views.LogoutView.as_view(), name='logout'),
    path('register', UserRegistrationApiView.as_view(), name='register'),
    path('', home, name='home'),
    path('contacts', ContactList.as_view(), name='contacts'),
]
