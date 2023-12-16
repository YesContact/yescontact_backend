from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from users.serializers import PasswordResetSerializer

password_reset_responses = {
    200: openapi.Response(
        description="Success",
        schema=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "detail": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="Password reset email has been sent.",
                    default="Password reset email has been sent.",
                )
            }
        ),
    ),
    400: openapi.Response(
        description="Bad Request",
        schema=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "detail": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="Validation errors or invalid request.",
                    default="Validation errors or invalid request.",
                )
            }
        ),
    ),
}


def password_reset_swagger_schema(request_body=PasswordResetSerializer):
    return swagger_auto_schema(
        responses=password_reset_responses,
        request_body=request_body,
    )
