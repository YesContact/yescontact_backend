from drf_spectacular.utils import extend_schema
from rest_framework import generics

from survey.serializers import SurveyUserCreateSerializer, SurveyUserListSerializer, SurveyUserDetailSerializer
from users.models import CustomUser


@extend_schema(tags=['Api Survey User'])
class SurveyUserCreateView(generics.CreateAPIView):
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
class SurveyUserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = SurveyUserDetailSerializer

    # Применение декоратора ко всем методам в классе
    # for method in http_method_names:
    #     locals()[method] = swagger_auto_schema(tags=['Api Survey User'])(getattr(super(), method))

    # @swagger_auto_schema(tags=['Api Survey User'])
    # def post(self, request, *args, **kwargs):
    #     return super().post(request, *args, **kwargs)
