from drf_spectacular.utils import extend_schema
from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated

from survey.permissions import IsOwnerOrReadOnlyUser
from survey.serializers import SurveyUserCreateSerializer, SurveyUserListSerializer, SurveyUserDetailSerializer
from users.models import CustomUser


@extend_schema(tags=['Api Survey User'])
class SurveyUserCreateView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    queryset = CustomUser.objects.all()
    serializer_class = SurveyUserCreateSerializer

    # @swagger_auto_schema(tags=['Api Survey User'])
    # @extend_schema(tags=['Api Survey User'])
    # def post(self, request, *args, **kwargs):
    #     return super().post(request, *args, **kwargs)


@extend_schema(tags=['Api Survey User'])
class SurveyUserListView(generics.ListAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = SurveyUserListSerializer

    # @extend_schema(tags=['Api Survey User'])
    # # @swagger_auto_schema(tags=['Api Survey User'])
    # def get(self, request, *args, **kwargs):
    #     return super().get(request, *args, **kwargs)


@extend_schema(tags=['Api Survey User'])
class SurveyUserDetailView(generics.RetrieveUpdateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = SurveyUserDetailSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnlyUser]

    # Применение декоратора ко всем методам в классе
    # for method in http_method_names:
    #     locals()[method] = swagger_auto_schema(tags=['Api Survey User'])(getattr(super(), method))

    # @swagger_auto_schema(tags=['Api Survey User'])
    # def post(self, request, *args, **kwargs):
    #     return super().post(request, *args, **kwargs)
