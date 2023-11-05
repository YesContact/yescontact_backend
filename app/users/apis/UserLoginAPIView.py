from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from users.models import CustomUser
from django.contrib.auth.forms import PasswordResetForm

from users.serializers import UserLoginSerializer


class UserLoginAPIView(APIView):
    serializer_class = UserLoginSerializer

    def post(self, request):
        phone_number = request.data.get("phone_number", None)
        password = request.data.get("password", None)
        if phone_number and password:
            user_obj = CustomUser.objects.filter(
                phone_number__iexact=phone_number
            ).first()

            if user_obj and user_obj.check_password(password):
                user = UserLoginSerializer(user_obj)
                data_list = {}
                data_list.update(user.data)
                return Response(
                    {"message": "Login Successfully", "data": data_list, "code": 200}
                )
            else:
                message = "Unable to login with given credentials"
                return Response({"message": message, "code": 500, "data": {}})
        else:
            message = "Invalid login details."
            return Response({"message": message, "code": 500, "data": {}})
