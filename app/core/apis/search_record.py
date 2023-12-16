from rest_framework import viewsets, permissions
from rest_framework.response import Response
from app.utils import send_notification, perform_search_action
from core.models import SearchRecord
from core.serializers import SearchRecordSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication

class SearchRecordViewSet(viewsets.ViewSet):
    serializer_class = SearchRecordSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    

    def create(self, request):
        # search_query = request.data.get('search_query')
        user1 = request.user
        user2 = request.data.get('user2')
        print(user1, user2)
        perform_search_action(user1, user2)
        return Response({'message': 'success'})