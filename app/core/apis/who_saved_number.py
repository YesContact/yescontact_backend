from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
from core.models import Contact
from core.serializers import ContactSerializer
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
import jwt, datetime
from rest_framework_simplejwt.authentication import JWTAuthentication
User = get_user_model()

class WhoSavedMNViewSet(viewsets.ModelViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = (IsAuthenticated,)
    serializer_class = ContactSerializer

    def list(self, request):
        user = request.user
        phone_number = user.phone_number

        search_results = Contact.objects.filter(phone_number=phone_number)
        serializer = ContactSerializer(search_results, many=True)
        # Filter out contacts with empty 'full_name' fields
        filtered_data = [contact for contact in serializer.data if contact.get('full_name') != '']
        return Response(filtered_data)

    def create(self, request):
        user = request.user
        phone_number = user.phone_number

        search_results = Contact.objects.filter(phone_number=phone_number)
        serializer = ContactSerializer(search_results, many=True)
        # Filter out contacts with empty 'full_name' fields
        filtered_data = [contact for contact in serializer.data if contact.get('full_name') != '']
        return Response(filtered_data)