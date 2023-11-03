from django.urls import path
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView, PasswordResetCompleteView

from users.views import *


urlpatterns = [
    path('', home, name='home'),
    path('login', login, name='login'),
    path('logout', auth_views.LogoutView.as_view(), name='logout'),
    path('password_reset/', PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password_reset/complete/', PasswordResetCompleteView.as_view(), name='password_reset_complete')
]
