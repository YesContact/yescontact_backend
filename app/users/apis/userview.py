from drf_spectacular.utils import extend_schema, OpenApiResponse
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication

from users.serializers import UserLoginSerializer


class UserViewSet(viewsets.ViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = (IsAuthenticated,)

    @extend_schema(
        responses={
            200: OpenApiResponse(response={"description": "Success", "example": {"message": "Login Successfully", "data": {"username": "User's username", "email": "User's email"}, "code": "HTTP status code"}},
                                 description="Success"),
        }
    )
    def get(self, request):
        user = request.user
        serializer = UserLoginSerializer(user)
        data = serializer.data
        return Response({"message": "Login Successfully", "data": data, "code": 200})
