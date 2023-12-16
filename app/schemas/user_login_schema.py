from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from users.serializers import UserLoginSerializer

user_login_responses = {
    200: openapi.Response(
        description="Success",
        schema=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "message": openapi.Schema(type=openapi.TYPE_STRING, description="Login Successfully", default='Login Successfully'),
                "token": openapi.Schema(type=openapi.TYPE_STRING, description="your_access_token_here", default='eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzAyNzM0MTEwLCJpYXQiOjE3MDI3MzA1MTAsImp0aSI6ImQyMjgzYzhhNTcyZTQ0YzE5NWU3MDk4MGY0ZTMyM2I4IiwidXNlcl9pZCI6Mn0.rx4nT8Qe51K2GmVvEmb64eITJeIKhlE9pMHuCFV9wbo'),
                "data": openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "phone_number": openapi.Schema(type=openapi.TYPE_STRING, description="Phone", default='+829321312')
                    }
                ),
                "code": openapi.Schema(type=openapi.TYPE_INTEGER, description="200", default='200')
            }
        ),
    ),
    401: openapi.Response(
        description="Unauthorized",
        schema=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "message": openapi.Schema(type=openapi.TYPE_STRING, description="Invalid phone number or password", default='Invalid phone number or password'),
                "code": openapi.Schema(type=openapi.TYPE_INTEGER, description="401", default='401')
            }
        ),
    ),
    400: openapi.Response(
        description="Bad Request",
        schema=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "error": openapi.Schema(type=openapi.TYPE_STRING, description="Your error message here"),
                "code": openapi.Schema(type=openapi.TYPE_INTEGER, description="400", default='400')
            }
        ),
    ),
}


def user_login_swagger_schema(request_body=UserLoginSerializer):
    return swagger_auto_schema(
        responses=user_login_responses,
        request_body=request_body
    )
