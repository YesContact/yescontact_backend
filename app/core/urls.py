from django.urls import path, include
from django.contrib.auth import views as auth_views

from .views import *
from .apis import *
from .serializers import *

urlpatterns = [
    path('contacts', ContactList.as_view({'get': 'list', 'post': 'create',}), name='contacts'),
]
