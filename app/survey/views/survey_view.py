from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from ..models import SurveyView, Survey
from ..serializers import SurveyViewApiSerializer


@extend_schema(
    parameters=[
        OpenApiParameter(name='survey_id', type=int, description='Specify id of survey to get count of views',
                         required=True),
    ],
    responses={200: openapi.Schema(type=openapi.TYPE_OBJECT,
                                   properties={'count': openapi.Schema(type=openapi.TYPE_INTEGER)})},
    tags=['Api Survey View']
)
class SurveyGetViewApi(ListAPIView):
    serializer_class = SurveyViewApiSerializer

    # @swagger_auto_schema(
    #     manual_parameters=[
    #         openapi.Parameter(
    #             'survey_id',
    #             openapi.IN_QUERY,
    #             description="Specify id of survey to get count of views",
    #             type=openapi.TYPE_INTEGER,
    #             required=True
    #         ),
    #     ],
    #     responses={200: openapi.Schema(type=openapi.TYPE_OBJECT,
    #                                    properties={'count': openapi.Schema(type=openapi.TYPE_INTEGER)})},
    #     tags=['Api Survey View']
    # )
    def get(self, request, *args, **kwargs):
        survey_id = self.request.query_params.get('survey_id')
        survey = Survey.objects.filter(id=survey_id).first()

        if not survey_id:
            raise ValidationError('Survey ID is missing in query parameters')

        if not survey:
            raise ValidationError('Survey with this id not found')

        queryset = SurveyView.objects.filter(survey=survey_id)
        count = queryset.count()

        response_data = {
            'count': count
        }

        return Response(response_data)


@extend_schema(
    parameters=[
        OpenApiParameter(name='survey_id', type=int, description='Specify id of survey to add new view',
                         required=True),
    ],
    responses={201: SurveyViewApiSerializer},
    tags=['Api Survey View']
)
class AddSurveyViewApi(APIView):
    # @swagger_auto_schema(
    #     manual_parameters=[
    #         openapi.Parameter(
    #             'survey_id',
    #             openapi.IN_QUERY,
    #             description="Specify id of survey to add new view",
    #             type=openapi.TYPE_INTEGER,
    #             required=True
    #         ),
    #     ],
    #     responses={201: SurveyViewApiSerializer},
    #     tags=['Api Survey View']
    # )
    def post(self, request, *args, **kwargs):
        survey_id = self.request.query_params.get('survey_id')
        try:
            survey = Survey.objects.get(id=survey_id)
        except Survey.DoesNotExist:
            return Response({"message": "Survey not found"}, status=status.HTTP_404_NOT_FOUND)

        exists_survey_view = SurveyView.objects.filter(survey=survey, user=request.user).first()
        if exists_survey_view:
            return Response({"message": "View is already added"}, status=status.HTTP_404_NOT_FOUND)

        survey_view = SurveyView(survey=survey, user=request.user)
        survey_view.save()

        serializer = SurveyViewApiSerializer(survey_view)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
