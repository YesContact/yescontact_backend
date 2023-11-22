from django.urls import path

from .views import *
from .apis import *
from .serializers import *

urlpatterns = [
    path('contacts', ContactList.as_view({'get': 'list', 'post': 'create',}), name='contacts'),
    path('take-numbers', TakingNumbersViewSet.as_view({'get': 'list', 'post': 'create',}), name='take-numbers'),
]
