from django.contrib.auth import get_user_model
from drf_spectacular.utils import extend_schema, OpenApiResponse
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication

from core.models import Contact
from core.serializers import ContactSerializer

User = get_user_model()


class WhoSavedMNViewSet(viewsets.ViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = (IsAuthenticated,)
    serializer_class = ContactSerializer

    @extend_schema(
        responses={
            200: OpenApiResponse(response={"description": "Success", "example": {"full_name": "Contact's full name"}},
                                 description="Success"),
        }
    )
    def list(self, request):
        user = request.user
        phone_number = user.phone_number

        search_results = Contact.objects.filter(phone_number=phone_number)
        serializer = ContactSerializer(search_results, many=True)
        # Filter out contacts with empty 'full_name' fields
        filtered_data = [
            contact for contact in serializer.data if contact.get("full_name") != ""
        ]
        return Response(filtered_data)

    @extend_schema(
        request=ContactSerializer,
        responses={
            200: OpenApiResponse(response={"description": "Success", "example": {"full_name": "Contact's full name"}},
                                 description="Success"),
        }
    )
    # @who_saved_mn_create_responses_swagger_schema()
    def create(self, request):
        user = request.user
        phone_number = user.phone_number

        search_results = Contact.objects.filter(phone_number=phone_number)
        serializer = ContactSerializer(search_results, many=True)
        # Filter out contacts with empty 'full_name' fields
        filtered_data = [
            contact for contact in serializer.data if contact.get("full_name") != ""
        ]
        return Response(filtered_data)
