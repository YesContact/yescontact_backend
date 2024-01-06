from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from ..models import Survey
from ..serializers import SurveyApiSerializer


@extend_schema(
    parameters=[
        OpenApiParameter(name='survey_id', type=int, description='Specify id of survey to share it', required=True),
    ],
    responses={201: SurveyApiSerializer},
    tags=['Api Survey Share']
)
class ShareSurveyApi(APIView):

    # @swagger_auto_schema(
    #     manual_parameters=[
    #         openapi.Parameter(
    #             'survey_id',
    #             openapi.IN_QUERY,
    #             description="Specify id of survey to share it",
    #             type=openapi.TYPE_INTEGER,
    #             required=True
    #         ),
    #     ],
    #     responses={201: SurveyApiSerializer},
    #     tags=['Api Survey Share']
    # )
    def get(self, request, *args, **kwargs):
        survey_id = self.request.query_params.get('survey_id')
        try:
            survey = Survey.objects.get(id=survey_id)
        except Survey.DoesNotExist:
            return Response({"message": "Survey not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = SurveyApiSerializer(survey)
        return Response(serializer.data, status=status.HTTP_200_OK)
