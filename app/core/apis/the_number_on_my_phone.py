from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets, status
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from core.models import Contact
from core.serializers import TheNumbersOnMyPhoneSerializer

User = get_user_model()


class TheNumbersOnMyPhone(viewsets.ModelViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = (IsAuthenticated,)
    serializer_class = TheNumbersOnMyPhoneSerializer

    def list(self, request):
        user = request.user

        phones = Contact.objects.filter(user=user)
        serializer = TheNumbersOnMyPhoneSerializer(phones, many=True)
        return Response(serializer.data)
    
    def create(self, request):
        user = request.user
        data = request.data  # Assuming data is a list of dictionaries

        # Serialize each dictionary in the list
        serialized_data = []
        for entry in data:
            serializer = TheNumbersOnMyPhoneSerializer(data=entry)
            serializer.is_valid(raise_exception=True)
            serialized_data.append(serializer.validated_data)

        # Create instances using the serialized data
        instances = []
        for entry_data in serialized_data:
            instance = Contact.objects.create(user=user, **entry_data)
            instances.append(instance)

        # Return a response with the serialized data of the created instances
        response_serializer = TheNumbersOnMyPhoneSerializer(instances, many=True)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)

