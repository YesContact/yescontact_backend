from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from core.models import Contact
from core.serializers import ContactSerializer


User = get_user_model()

class TheNumbersOnMyPhone(viewsets.ModelViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = (IsAuthenticated,)
    serializer_class = ContactSerializer

    def list(self, request):
        user = request.user

        phones = Contact.objects.filter(user=user)
        serializer = ContactSerializer(phones, many=True)
        return Response(serializer.data)