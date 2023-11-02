from django.urls import path

from .views import (
    UserRegistrationApiView, 
    UserLoginAPIView, 
    PasswordResetAPI
    )

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView
    )


urlpatterns = [
    path('register/', UserRegistrationApiView.as_view(), name='register'),
    path('login/', UserLoginAPIView.as_view(), name='login'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('password_reset/', PasswordResetAPI.as_view(), name='password_reset_api'),

]