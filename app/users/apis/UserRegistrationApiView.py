from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from users.models import CustomUser
from django.contrib.auth.forms import PasswordResetForm

from users.serializers import UserRegistrationSerializer
from django.conf import settings
from app.utils import generate_otp, send_otp_email 

class UserRegistrationApiView(CreateAPIView):
    serializer_class = UserRegistrationSerializer

    def perform_create(self, serializer):
        instance = serializer.save()
        instance.set_password(instance.password)
        instance.save()

        # generate otp
        otp = generate_otp()
        instance.otp = otp
        instance.is_verified = False
        instance.save()

        # send otp to user
        send_otp_email(instance.email, otp)
