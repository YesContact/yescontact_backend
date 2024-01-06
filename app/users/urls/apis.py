from django.urls import path

from users.apis import UserRegistrationApiView, UserLoginViewSet, PasswordResetAPI, OTPVerificationAPI, UserViewSet, LogoutViewSet

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


urlpatterns = [
    path("register/", UserRegistrationApiView.as_view(), name="register"),
    path("login/", UserLoginViewSet.as_view(), name="login"),
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("password_reset/", PasswordResetAPI.as_view(), name="password_reset_api"),
    path("otp_verification/", OTPVerificationAPI.as_view(), name="otp_verification_api"),
    path('user-view/', UserViewSet.as_view({'get': 'get'}), name='user-view'),
    path('logout/', LogoutViewSet.as_view(), name='logout'),
]
