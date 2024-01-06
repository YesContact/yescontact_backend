from drf_spectacular import openapi
from drf_spectacular.types import OpenApiTypes
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from users.models import CustomUser
from django.contrib.auth.forms import PasswordResetForm
from drf_spectacular.utils import extend_schema, OpenApiResponse

from users.serializers import PasswordResetSerializer


class PasswordResetAPI(GenericAPIView):
    permission_classes = (IsAuthenticated,)

    @extend_schema(
        request=PasswordResetSerializer,
        responses={
            200: OpenApiResponse(response={"description": "Success", "example": {"message": "Password reset email has "
                                                                                            "been sent."}},
                                 description="Success"),
            400: OpenApiResponse(response={"description": "Bad Request", "example": {"message": "Validation errors or "
                                                                                                "invalid request."}},
                                 description="Bad Request"),
            404: OpenApiResponse(response={"description": "Not Found", "example": {"message": "You have not registered yet"}},
                                 description="Not Found"),
        }
    )
    def post(self, request):
        serializer = PasswordResetSerializer(data=request.data)

        if serializer.is_valid():
            email = serializer.validated_data["email"]
            form = PasswordResetForm(data={"email": email})
            user_obj = CustomUser.objects.filter(email__iexact=email).first()

            if form.is_valid():
                if user_obj:
                    form.save(request=request)
                    return Response({"detail": "Password reset email has been sent."}, status=404)
                else:
                    return Response({"detail": "You have not registered yet"}, status=404)
            else:
                return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
