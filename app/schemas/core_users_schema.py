from drf_yasg import openapi

from core.serializers import ContactSerializer
from drf_yasg.utils import swagger_auto_schema

who_saved_mn_list_responses = {
    200: openapi.Response(
        description="Success",
        schema=openapi.Schema(
            type=openapi.TYPE_ARRAY,
            items=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "full_name": openapi.Schema(
                        type=openapi.TYPE_STRING,
                        description="Contact's full name",
                    ),
                },
            ),
        ),
    )
}


def who_saved_mn_list_responses_swagger_schema(request_body=ContactSerializer):
    return swagger_auto_schema(
        responses=who_saved_mn_list_responses,
    )


who_saved_mn_create_responses = {
    200: openapi.Response(
        description="Success",
        schema=openapi.Schema(
            type=openapi.TYPE_ARRAY,
            items=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "full_name": openapi.Schema(
                        type=openapi.TYPE_STRING,
                        description="Contact's full name",
                    ),
                },
            ),
        ),
    )
}


def who_saved_mn_create_responses_swagger_schema(request_body=ContactSerializer):
    return swagger_auto_schema(
        responses=who_saved_mn_create_responses,
        request_body=request_body,
    )
