from drf_spectacular.utils import extend_schema, OpenApiResponse
from rest_framework import viewsets
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.views import APIView


class LogoutViewSet(APIView):
    @extend_schema(
        responses={
            200: OpenApiResponse(response={"description": "Success", "example": {"message": "Logout Successfully",
                                                                                 "code": 200}}, description="Success"),
        }
    )
    def post(self, request):
        response = Response()
        response.delete_cookie("jwt")
        response.data = {"message": "Logout Successfully", "code": 200}
        return response
