from rest_framework import viewsets
from rest_framework.response import Response
from users.models import CustomUser
from users.serializers import UserLoginSerializer
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.permissions import AllowAny


class UserLoginViewSet(viewsets.ViewSet):
    permission_classes = [AllowAny]
    serializer_class = UserLoginSerializer

    def create(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            phone_number = serializer.validated_data.get("phone_number")
            password = serializer.validated_data.get("password")

            user_obj = CustomUser.objects.filter(
                phone_number__iexact=phone_number
            ).first()

            if user_obj and user_obj.check_password(password):
                access_token = AccessToken.for_user(user_obj)
                serializer = UserLoginSerializer(user_obj)
                data = serializer.data

                return Response(
                    {
                        "message": "Login Successfully",
                        "token": str(access_token),
                        "data": data,
                        "code": 200,
                    }
                )
            else:
                message = "Invalid phone number or password"
                return Response(
                    {"message": message, "code": 401}
                )  # Unauthorized status code
        else:
            return Response(serializer.errors, status=400)
