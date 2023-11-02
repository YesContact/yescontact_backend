from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from users.models import CustomUser
from django.contrib.auth.forms import PasswordResetForm

from .serializers import (
    UserRegistrationSerializer, 
    UserLoginSerializer, 
    PasswordResetSerializer
    )



class UserRegistrationApiView(CreateAPIView):
   serializer_class = UserRegistrationSerializer

   def perform_create(self, serializer):
        instance = serializer.save()
        instance.set_password(instance.password)
        instance.save()


class UserLoginAPIView(APIView):
    permission_classes = (IsAuthenticated, )

    def post(self,request): 
        phone_number = request.data.get('phone_number',None)
        password = request.data.get('password',None)
        if phone_number and password:
            user_obj = CustomUser.objects.filter(phone_number__iexact=phone_number).first()
            
            if user_obj and user_obj.check_password(password):
                user = UserLoginSerializer(user_obj)
                data_list = {}
                data_list.update(user.data)
                return Response({"message": "Login Successfully", "data":data_list, "code": 200})
            else:
                message = "Unable to login with given credentials"
                return Response({"message": message , "code": 500, 'data': {}} )
        else:
            message = "Invalid login details."
            return Response({"message": message , "code": 500, 'data': {}})


class PasswordResetAPI(APIView):
    permission_classes = (IsAuthenticated, )
    def post(self, request):
        serializer = PasswordResetSerializer(data=request.data)

        if serializer.is_valid():
            email = serializer.validated_data['email']
            form = PasswordResetForm(data={'email': email})
            user_obj = CustomUser.objects.filter(email__iexact=email).first()

            if form.is_valid():
                if user_obj:
                    form.save(request=request)
                    return Response({'detail': 'Password reset email has been sent.'})
                else :
                    return Response({'detail': 'You have not registered yet'})
            else:
                return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

