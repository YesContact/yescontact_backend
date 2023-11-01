from django.urls import path, include
from django.contrib.auth import views as auth_views

from .views import *
from .apis import *
from .serializers import *

urlpatterns = [
    path('login', login, name='login'),
    path('logout', auth_views.LogoutView.as_view(), name='logout'),
    path('register', UserRegistrationViewSet.as_view({'get': 'list', 'post': 'create',}), name='register'),
    path('', home, name='home'),
    path('contacts', ContactList.as_view({'get': 'list', 'post': 'create',}), name='contacts'),
]
