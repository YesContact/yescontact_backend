from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from users.serializers import OTPVerificationSerializer

otp_verification_responses = {
    200: openapi.Response(
        description="Success",
        schema=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "message": openapi.Schema(type=openapi.TYPE_STRING, description="OTP verified successfully", default='OTP verified successfully'),
            }
        ),
    ),
    400: openapi.Response(
        description="Bad Request",
        schema=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "message": openapi.Schema(type=openapi.TYPE_STRING, description="Invalid OTP", default='Invalid OTP'),
            }
        ),
    ),
    404: openapi.Response(
        description="Not Found",
        schema=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "message": openapi.Schema(type=openapi.TYPE_STRING, description="User not found", default='User not found'),
            }
        ),
    ),
}


def otp_verification_swagger_schema(request_body=OTPVerificationSerializer):
    return swagger_auto_schema(
        responses=otp_verification_responses,
        request_body=request_body,
    )
