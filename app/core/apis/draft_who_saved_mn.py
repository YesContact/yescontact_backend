from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import status
from rest_framework.response import Response
from rest_framework import viewsets
from core.models import Contact
from core.serializers import ContactSerializer
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema


class WhoSavedViewSet(viewsets.ModelViewSet):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer

    # @swagger_auto_schema(
    #     manual_parameters=[
    #         openapi.Parameter(
    #             "phone_number", in_=openapi.IN_QUERY, type=openapi.TYPE_INTEGER
    #         )
    #     ]
    # )
    @extend_schema(
        parameters=[
            OpenApiParameter(name='phone_number', type=int, description='Specify the phone number', required=True),
        ]
    )
    def list(self, request, *args, **kwargs):
        phone_number = request.query_params.get("phone_number", None)
        if phone_number:
            try:
                if Contact.objects.filter(phone_number=phone_number).exists():
                    queryset = Contact.objects.filter(phone_number=phone_number)
                    serializer = ContactSerializer(queryset, many=True)
                    if "full_name" in serializer.data[0]:
                        for contact in serializer.data:
                            del contact["full_name"]
                    return Response(serializer.data)

            except ValueError:
                return Response(
                    {"message": "Invalid phone_number provided"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        else:
            return Response(
                {"message": "phone_number is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )
