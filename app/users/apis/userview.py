from rest_framework import viewsets
from rest_framework.response import Response
from users.models import CustomUser
from users.serializers import UserLoginSerializer
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
import jwt, datetime
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication


class UserViewSet(viewsets.ViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        user = request.user
        serializer = UserLoginSerializer(user)
        data = serializer.data
        return Response({"message": "Login Successfully", "data": data, "code": 200})
