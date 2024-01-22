from django.utils import timezone
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from ..models import Survey, SurveyVote, SurveyOption, CompletedSurvey
from ..serializers import SurveyVoteApiSerializer


def submit_survey(survey):
    completed_survey = CompletedSurvey(
        survey=survey,
        completed_at=timezone.now()
    )
    completed_survey.save()

    options = SurveyOption.objects.filter(survey=survey).all()
    total_dict = {

    }
    # for option in options:
    #     votes = SurveyVote.objects.filter(survey_option=option).all()
    #     total_price = 0
    #     for vote in votes:
    #         total_price += vote.ammount
    #
    #     total_dict[option.id] = {
    #         'votes': len(votes),
    #         'total_price': 0
    #     }
    #     total_dict[option.id] =
    #
    # print(total_dict)




    pass


@extend_schema(
    parameters=[
        OpenApiParameter(name='survey_option_id', type=int,
                         description='Specify id of survey option to get by survey_option_id', required=True),
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
        OpenApiParameter(name='amount', type=int,
                         description='Specify amount of jetons to vote (if survey is free, ignore this field)'),
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
        amount = self.request.query_params.get('amount')
        try:
            survey_option = SurveyOption.objects.get(id=survey_option_id)
        except SurveyOption.DoesNotExist:
            return Response({"message": "Survey option not found"}, status=status.HTTP_404_NOT_FOUND)

        try:
            survey = Survey.objects.get(id=survey_option.survey.id)
        except Survey.DoesNotExist:
            return Response({"message": "Survey not found"}, status=status.HTTP_404_NOT_FOUND)

        print(survey.check_completed)
        if survey.check_completed:
            return Response({"message": "Survey is completed"}, status=status.HTTP_404_NOT_FOUND)

        if survey.paid:
            if not amount:
                return Response({"message": "Amount is missing in paid survey"},
                                status=status.HTTP_404_NOT_FOUND)

            try:
                amount = float(amount)
            except ValueError:
                return Response({"message": "Amount must be a number"},
                                status=status.HTTP_404_NOT_FOUND)

            print(amount)

            if not 0.1 < amount < 1300:
                return Response({"message": "Amount must be greater than 0.1 and less than 1300"},
                                status=status.HTTP_404_NOT_FOUND)

            if request.user.wallet < amount:
                return Response({"message": "Not enough jetons to vote"}, status=status.HTTP_404_NOT_FOUND)

        exists_survey_vote = SurveyVote.objects.filter(survey_option=survey_option, user=request.user,
                                                       survey=survey).first()
        if exists_survey_vote:
            return Response({"message": "Vote is already added"}, status=status.HTTP_404_NOT_FOUND)

        all_votes = SurveyVote.objects.filter(survey=survey).count()
        if survey.vote_limit and all_votes >= survey.vote_limit:
            submit_survey(survey=survey)
            return Response({"message": "Max votes reached"}, status=status.HTTP_404_NOT_FOUND)

        survey_vote = SurveyVote(survey_option=survey_option, user=request.user, survey=survey, amount=amount)
        survey_vote.save()

        serializer = SurveyVoteApiSerializer(survey_vote)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
