from django.contrib.auth.models import User
from rest_framework.renderers import MultiPartRenderer
from rest_framework.templatetags import rest_framework
from users.models import CustomUser  # Import your custom user model
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.exceptions import ValidationError
from rest_framework.generics import ListAPIView, CreateAPIView
from datetime import timedelta
from django.utils import timezone

from ..serializers import CreateSurveyOptionApiSerializer
from ..tasks import expire_survey
from ..models import SurveyOption, Survey
from ..serializers import SurveyOptionApiSerializer, CreateSurveyApiSerializer


class SurveyOptionApiView(ListAPIView):
    queryset = SurveyOption.objects.all()
    serializer_class = SurveyOptionApiSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        survey_id = self.request.query_params.get('survey_id')
        if not survey_id:
            raise ValidationError('Specify survey_id parameter')

        exist_survey = Survey.objects.filter(id=survey_id)
        if not exist_survey.exists():
            raise ValidationError('Survey with this id not found')

        queryset = queryset.filter(survey=exist_survey.first())

        return queryset

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'survey_id',
                openapi.IN_QUERY,
                description="Specify id of survey to get all options",
                type=openapi.TYPE_INTEGER,
                required=True
            ),
        ],
        responses={200: SurveyOptionApiSerializer(many=True)}
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class CreateSurveyApiView(CreateAPIView):
    queryset = SurveyOption.objects.all()
    serializer_class = CreateSurveyApiSerializer

    @swagger_auto_schema(
        request_body=CreateSurveyApiSerializer,
        responses={200: CreateSurveyApiSerializer},
        tags=['Api Survey']
    )
    def post(self, request, *args, **kwargs):
        # serializer = self.get_serializer(data=request.data)
        # serializer.is_valid(raise_exception=True)
        # serializer.save()

        # new_survey = serializer.save(
        #     deadline=timezone.now() + timedelta(days=1)
        # )

        # expire_survey.apply_async((new_survey.id,), eta=new_survey.deadline)
        return super().post(request, *args, **kwargs)


class CreateSurveyOptionApiView(CreateAPIView):
    """
        Go to this endpoint to upload image_file of option
    """
    queryset = SurveyOption.objects.all()
    serializer_class = CreateSurveyOptionApiSerializer

    @swagger_auto_schema(
        request_body=CreateSurveyOptionApiSerializer,
        responses={200: CreateSurveyOptionApiSerializer},
        tags=['Api Survey Option']
    )
    def post(self, request, *args, **kwargs):
        # serializer = self.get_serializer(data=request.data)
        # if serializer.is_valid():
        return super().post(request, *args, **kwargs)

