from django.urls import path

from core.views import *
from core.apis import *
from core.serializers import *
from users.apis import *
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register("users", WhoSavedMNViewSet, basename="users")
router.register('search-record', SearchRecordViewSet, basename='search-record')


urlpatterns = [
    path('contacts/', ContactList.as_view({'get': 'list', 'post': 'create',}), name='contacts'),
    path('take-numbers/', TakingNumbersViewSet.as_view({'get': 'list', 'post': 'create',}), name='take-numbers'),
    path('who-saved-mn/', WhoSavedMNViewSet.as_view({'get': 'list', 'post': 'create'}), name='who-saved-mn'),
    path('the-numbers-on-my-phone/', TheNumbersOnMyPhone.as_view({'get': 'list', 'post': 'create'}), name='the-numbers-on-my-phone'),
    path('search-record/', SearchRecordViewSet.as_view({'post': 'create'}), name='search-record'),
]


urlpatterns += router.urls