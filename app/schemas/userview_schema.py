from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from users.serializers import UserLoginSerializer

user_get_responses = {
    200: openapi.Response(
        description="Success",
        schema=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "message": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="Login Successfully",
                    default="Login Successfully",
                ),
                "data": openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    description="User data",
                    properties={
                        "username": openapi.Schema(
                            type=openapi.TYPE_STRING,
                            description="User's username",
                        ),
                        "email": openapi.Schema(
                            type=openapi.TYPE_STRING,
                            description="User's email",
                        ),
                        # Add other user-related properties here based on serializer
                    },
                ),
                "code": openapi.Schema(
                    type=openapi.TYPE_INTEGER,
                    description="HTTP status code",
                    default=200,
                ),
            },
        ),
    ),
}


def userview_swagger_schema(request_body=UserLoginSerializer):
    return swagger_auto_schema(
        responses=user_get_responses,
    )
