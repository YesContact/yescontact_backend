from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from users.models import CustomUser
from django.contrib.auth.forms import PasswordResetForm

from users.serializers import PasswordResetSerializer

from schemas.password_reset_schema import password_reset_swagger_schema


class PasswordResetAPI(APIView):
    permission_classes = (IsAuthenticated,)

    @password_reset_swagger_schema()
    def post(self, request):
        serializer = PasswordResetSerializer(data=request.data)

        if serializer.is_valid():
            email = serializer.validated_data["email"]
            form = PasswordResetForm(data={"email": email})
            user_obj = CustomUser.objects.filter(email__iexact=email).first()

            if form.is_valid():
                if user_obj:
                    form.save(request=request)
                    return Response({"detail": "Password reset email has been sent."})
                else:
                    return Response({"detail": "You have not registered yet"})
            else:
                return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
