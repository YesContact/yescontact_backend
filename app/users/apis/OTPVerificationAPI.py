from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from users.models import CustomUser
from users.serializers import OTPVerificationSerializer


class OTPVerificationAPI(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = OTPVerificationSerializer

    def post(self, request):
        email = request.data.get("email")
        otp = request.data.get("otp")

        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            return Response({"message": "User not found"}, status=404)

        if user.otp == otp:
            user.is_verified = True  # Mark user as verified
            user.save()
            return Response({"message": "OTP verified successfully"})
        else:
            return Response({"message": "Invalid OTP"}, status=400)
