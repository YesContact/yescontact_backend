from django.contrib.auth import get_user_model
from drf_spectacular.utils import extend_schema, OpenApiResponse
from rest_framework import viewsets, status
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
            200: OpenApiResponse(
                response={
                    "description": "Success",
                    "example": {"full_name": "Contact's full name"},
                },
                description="Success",
            ),
        }
    )
    def list(self, request):
        user = request.user

        if not user or not user.full_name:
            return Response(
                {"detail": "User object does not exist or has no full_name."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        contacts = Contact.objects.filter(full_name__icontains=user.full_name)
        serializer = ContactSerializer(contacts, many=True)

        phone_number_mapping = self.get_phone_number_mapping()
        # print(phone_number_mapping)

        data = []
        for contact in serializer.data:
            contact_user = contact["user"]
            try:
                if contact_user in phone_number_mapping:
                    contact_phone_number = phone_number_mapping[contact_user]
                    data.append(
                        {
                            "id": contact["id"],
                            "phone_number": contact_phone_number,
                            "full_name": contact["full_name"],
                            "user": contact_user,
                        }
                    )
            except Contact.DoesNotExist:
                return Response(
                    {"detail": "Contact object does not exist."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        return Response(data)

    def get_phone_number_mapping(self):
        users = User.objects.filter(phone_number__isnull=False).values(
            "full_name", "phone_number"
        )
        phone_number_mapping = {
            user["full_name"]: user["phone_number"] for user in users
        }
        return phone_number_mapping
