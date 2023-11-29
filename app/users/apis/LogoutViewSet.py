from rest_framework import viewsets
from rest_framework.response import Response


class LogoutViewSet(viewsets.ViewSet):
    def post(self, request):
        response = Response()
        response.delete_cookie("jwt")
        response.data = {"message": "Logout Successfully", "code": 200}
        return response
