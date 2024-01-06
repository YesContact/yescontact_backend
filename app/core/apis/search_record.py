from drf_spectacular.utils import OpenApiResponse, extend_schema
from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication

from app.utils import perform_search_action
from core.serializers import SearchRecordSerializer


class SearchRecordViewSet(viewsets.ViewSet):
    serializer_class = SearchRecordSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    @extend_schema(
        request=SearchRecordSerializer,
        responses={
            200: OpenApiResponse(
                response={"description": "Success", "example": {"message": "Search record created successfully"}},
                description="Success"),
        }
    )
    def create(self, request):
        # search_query = request.data.get('search_query')
        user1 = request.user
        user2 = request.data.get('user2')
        print(user1, user2)
        perform_search_action(user1, user2)
        return Response({'message': 'success'})
