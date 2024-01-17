from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from ..models import Survey, SurveyVote, SurveyOption
from ..serializers import SurveyVoteApiSerializer


@extend_schema(
    parameters=[
        OpenApiParameter(name='survey_option_id', type=int, description='Specify id of survey option to get by survey_option_id', required=True),
    ],
    responses={200: SurveyVoteApiSerializer(many=True)},
    tags=['Api Survey Vote']
)
class GetSurveyVoteApi(APIView):
    # permission_classes = [permissions.IsAuthenticated]
    # authentication_classes = [JWTAuthentication]
    # @swagger_auto_schema(
    #     manual_parameters=[
    #         openapi.Parameter(
    #             'survey_option_id',
    #             openapi.IN_QUERY,
    #             description="Specify id of survey option to add new vote",
    #             type=openapi.TYPE_INTEGER,
    #             required=True
    #         ),
    #     ],
    #     responses={201: SurveyVoteApiSerializer},
    #     tags=['Api Survey Vote']
    # )
    def get(self, request, *args, **kwargs):
        survey_option_id = self.request.query_params.get('survey_option_id')
        try:
            survey_option = SurveyOption.objects.get(id=survey_option_id)
        except SurveyOption.DoesNotExist:
            return Response({"message": "Survey option not found"}, status=status.HTTP_404_NOT_FOUND)

        try:
            survey = Survey.objects.get(id=survey_option.survey.id)
        except Survey.DoesNotExist:
            return Response({"message": "Survey not found"}, status=status.HTTP_404_NOT_FOUND)

        exists_survey_vote = SurveyVote.objects.filter(survey_option=survey_option, user=request.user,
                                                       survey=survey).first()
        if not exists_survey_vote:
            return Response({"message": "Vote not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = SurveyVoteApiSerializer(exists_survey_vote)
        return Response(serializer.data, status=status.HTTP_200_OK)


@extend_schema(
    parameters=[
        OpenApiParameter(name='survey_option_id', type=int, description='Specify id of survey option to add new vote',
                         required=True),
    ],
    responses={201: SurveyVoteApiSerializer},
    tags=['Api Survey Vote']
)
class AddSurveyVoteApi(APIView):
    # serializer_class = SurveyVoteApiSerializer

    # @swagger_auto_schema(
    #     manual_parameters=[
    #         openapi.Parameter(
    #             'survey_option_id',
    #             openapi.IN_QUERY,
    #             description="Specify id of survey option to add new vote",
    #             type=openapi.TYPE_INTEGER,
    #             required=True
    #         ),
    #     ],
    #     responses={201: SurveyVoteApiSerializer},
    #     tags=['Api Survey Vote']
    # )
    def post(self, request, *args, **kwargs):
        survey_option_id = self.request.query_params.get('survey_option_id')
        try:
            survey_option = SurveyOption.objects.get(id=survey_option_id)
        except SurveyOption.DoesNotExist:
            return Response({"message": "Survey option not found"}, status=status.HTTP_404_NOT_FOUND)

        try:
            survey = Survey.objects.get(id=survey_option.survey.id)
        except Survey.DoesNotExist:
            return Response({"message": "Survey not found"}, status=status.HTTP_404_NOT_FOUND)

        exists_survey_vote = SurveyVote.objects.filter(survey_option=survey_option, user=request.user,
                                                       survey=survey).first()
        if exists_survey_vote:
            return Response({"message": "Vote is already added"}, status=status.HTTP_404_NOT_FOUND)

        survey_vote = SurveyVote(survey_option=survey_option, user=request.user, survey=survey)
        survey_vote.save()

        serializer = SurveyVoteApiSerializer(survey_vote)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
