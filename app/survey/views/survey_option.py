from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.exceptions import ValidationError
from rest_framework.generics import ListAPIView

from ..models import SurveyOption, Survey
from ..serializers import SurveyOptionApiSerializer


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
