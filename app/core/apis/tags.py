from django.contrib.auth import get_user_model
from drf_spectacular.utils import extend_schema, OpenApiResponse
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication

from core.models import Contact
from core.serializers import ContactSerializer

User = get_user_model()


class TagViewSet(viewsets.ViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = (IsAuthenticated,)
    serializer_class = ContactSerializer

    @extend_schema(
        request=ContactSerializer,
        responses={
            200: OpenApiResponse(response={"description": "Success", "example": {"full_name": "Contact's full name"}},
                                 description="Success"),
        }
    )
    # @who_saved_mn_create_responses_swagger_schema()
    def create(self, request):
        phone_number = request.data.get("phone_number")

        if not phone_number:
            return Response({"phone_number": ["This field is required."]}, status=400)

        # Query the user's saved contacts to get the full names associated with the provided phone number
        contacts = Contact.objects.filter(phone_number=phone_number)

        if not contacts.exists():
            return Response({"detail": "Contact not found."}, status=status.HTTP_404_NOT_FOUND)

        # Retrieve the full names from the found contacts
        full_names = [contact.full_name for contact in contacts]

        return Response({"full_names": full_names})
        