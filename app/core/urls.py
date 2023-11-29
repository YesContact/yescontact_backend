from django.urls import path

from .views import *
from .apis import *
from .serializers import *
from users.apis import *
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register("users", WhoSavedMNViewSet, basename="users")


urlpatterns = [
    path('contacts/', ContactList.as_view({'get': 'list', 'post': 'create',}), name='contacts'),
    path('take-numbers/', TakingNumbersViewSet.as_view({'get': 'list', 'post': 'create',}), name='take-numbers'),
    path('who-saved-mn/', WhoSavedMNViewSet.as_view({'get': 'list', 'post': 'create'}), name='who-saved-mn'),
    path('the-numbers-on-my-phone/', TheNumbersOnMyPhone.as_view({'get': 'list'}), name='the-numbers-on-my-phone'),
]


urlpatterns += router.urls