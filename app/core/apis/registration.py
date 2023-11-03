from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from core.models import CustomUser  # Import your custom user model
from core.serializers import UserRegistrationSerializer  # Import your user registration serializer

class UserRegistrationViewSet(ModelViewSet):
    queryset = CustomUser.objects.all()  # Specify the queryset for your user model
    serializer_class = UserRegistrationSerializer

    def list(self, request, *args, **kwargs):
        queryset = CustomUser.objects.all()
        serializer = UserRegistrationSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
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
    
    
