from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from core.serializers import UserRegistrationSerializer


class UserRegistrationApiView(APIView):
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()
            user.email = serializer.validated_data["email"]
            user.full_name = serializer.validated_data["full_name"]
            user.phone_number = serializer.validated_data["phone_number"]
            user.set_password(serializer.validated_data["password"])
            user.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
