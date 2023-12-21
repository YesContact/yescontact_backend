from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.exceptions import ValidationError
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from ..models import Survey, Like
from ..serializers import SurveyLikeApiSerializer


class SurveyLikeApiView(ListAPIView):
    queryset = Like.objects.all()
    serializer_class = SurveyLikeApiSerializer

    # def get_queryset(self):
    #     queryset = super().get_queryset()
    #     survey_id = self.request.query_params.get('survey_id')
    #     if not survey_id:
    #         raise ValidationError('Specify survey_id parameter')
    #
    #     exist_survey = Survey.objects.filter(id=survey_id)
    #     if not exist_survey.exists():
    #         raise ValidationError('Survey with this id not found')
    #
    #     queryset = queryset.filter(survey=exist_survey.first())
    #
    #     return queryset

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'survey_id',
                openapi.IN_QUERY,
                description="Specify id of survey to get all likes",
                type=openapi.TYPE_INTEGER,
                required=True
            ),
        ],
        responses={200: SurveyLikeApiSerializer(many=True)},
        tags=['Api Survey Like']
    )
    def get(self, request, *args, **kwargs):
        survey_id = self.request.query_params.get('survey_id')

        survey = Survey.objects.filter(id=survey_id).first()

        if not survey_id:
            raise ValidationError('Survey ID is missing in query parameters')

        if not survey:
            raise ValidationError('Survey with this id not found')

        queryset = Survey.objects.filter(id=survey_id)
        count = queryset.count()

        response_data = {
            'count': count
        }

        return Response(response_data)
        # return super().get(request, *args, **kwargs)


class AddSurveyLikeApiView(APIView):
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'survey_id',
                openapi.IN_QUERY,
                description="Specify id of survey to add new like",
                type=openapi.TYPE_INTEGER,
                required=True
            ),
        ],
        responses={201: SurveyLikeApiSerializer},
        tags=['Api Survey Like']
    )
    def post(self, request, *args, **kwargs):
        survey_id = self.request.query_params.get('survey_id')
        try:
            survey = Survey.objects.get(id=survey_id)
        except Survey.DoesNotExist:
            raise ValidationError('Survey with this id not found')

        exists_like = Like.objects.filter(survey=survey, user=request.user).first()
        if exists_like:
            raise ValidationError('You have already add your like')

        like = Like(survey=survey, user=request.user)
        like.save()

        serializer = SurveyLikeApiSerializer(like)
        return Response(serializer.data)
