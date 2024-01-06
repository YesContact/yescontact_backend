from drf_spectacular import openapi
from drf_spectacular.utils import extend_schema, OpenApiResponse
from rest_framework import status
from rest_framework.fields import CharField
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.serializers import Serializer

from users.models import CustomUser
from users.serializers import OTPVerificationSerializer
from drf_spectacular.types import OpenApiTypes as oatypes, OpenApiTypes
from drf_spectacular.utils import OpenApiParameter, OpenApiResponse


class OTPVerificationAPI(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = OTPVerificationSerializer

    @extend_schema(
        responses={
            200: OpenApiResponse(response=OTPVerificationSerializer, description="OTP verified successfully"),
            400: OpenApiResponse(response={"description": "Bad Request", "example": {"message": "Invalid OTP"}},
                                 description="Bad Request"),
            404: OpenApiResponse(response={"description": "Not Found", "example": {"message": "User not found"}},
                                 description="Not Found"),
        }
    )
    def post(self, request):
        email = request.data.get("email")
        otp = request.data.get("otp")

        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            return Response({"message": "User not found"}, status=404)

        if user.otp == otp:
            user.is_verified = True  # Mark user as verified
            user.save()
            return Response({"message": "OTP verified successfully"}, status=200)
        else:
            return Response({"message": "Invalid OTP"}, status=400)
