from drf_spectacular.utils import extend_schema, OpenApiResponse
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken
from users.models import CustomUser
from users.serializers import UserLoginSerializer


class UserLoginViewSet(generics.GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = UserLoginSerializer

    @extend_schema(
        request=UserLoginSerializer,
        responses={
            200: OpenApiResponse(response={"description": "Success", "example": {"message": "Login Successfully",
                                                                                 "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzAyNzM0MTEwLCJpYXQiOjE3MDI3MzA1MTAsImp0aSI6ImQyMjgzYzhhNTcyZTQ0YzE5NWU3MDk4MGY0ZTMyM2I4IiwidXNlcl9pZCI6Mn0.rx4nT8Qe51K2GmVvEmb64eITJeIKhlE9pMHuCFV9wbo",
                                                                                 "data": {"phone_number": "+829321312"}, "code": 200}},
                                 description="Success"),
            401: OpenApiResponse(response={"description": "Unauthorized", "example": {"message": "Invalid phone number or password"}},
                                 description="Unauthorized")
        }
    )
    def post(self, request):
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
            return Response(serializer.errors, status=401)
