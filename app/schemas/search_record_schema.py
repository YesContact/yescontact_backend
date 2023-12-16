from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from users.serializers import OTPVerificationSerializer

from core.serializers import SearchRecordSerializer

search_record_create_responses = {
    200: openapi.Response(
        description="Success",
        schema=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "message": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="Search record created successfully",
                    default="Search record created successfully",
                )
            }
        ),
    )
}


def search_record_create_responses_swagger_schema(request_body=SearchRecordSerializer):
    return swagger_auto_schema(
        responses=search_record_create_responses,
        request_body=request_body,
    )