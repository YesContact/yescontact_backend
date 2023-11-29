from django.urls import path

from .views import *
from .apis import *
from .serializers import *
from users.apis import *
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register("users", WhoSavedMNViewSet, basename="users")
router.register("user-view", UserViewSet, basename="user-view")


urlpatterns = [
    path('contacts/', ContactList.as_view({'get': 'list', 'post': 'create',}), name='contacts'),
    path('take-numbers/', TakingNumbersViewSet.as_view({'get': 'list', 'post': 'create',}), name='take-numbers'),
    path('who-saved-mn/', WhoSavedMNViewSet.as_view({'get': 'list', 'post': 'create'}), name='who-saved-mn'),
]


urlpatterns += router.urls