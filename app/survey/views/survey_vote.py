from itertools import groupby

from django.db import transaction
from django.utils import timezone
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from ..models import Survey, SurveyVote, SurveyOption, CompletedSurvey
from ..serializers import SurveyVoteApiSerializer
from django.db.models import Max, Sum


@transaction.atomic
def submit_survey(survey):
    # completed_survey = CompletedSurvey(
    #     survey=survey,
    #     completed_at=timezone.now()
    # )
    # completed_survey.save()

    winning_option = SurveyOption.objects.filter(survey=survey).annotate(
        total_votes=Sum('vote_survey_option__amount')).order_by('-total_votes').first()

    total_price_except_winning_option = \
        SurveyVote.objects.filter(survey_option__survey=survey).exclude(survey_option=winning_option).aggregate(
            total_price=Sum('amount'))[
            'total_price']
    print(total_price_except_winning_option)

    owner_total = total_price_except_winning_option * 0.2
    print(owner_total)

    # 20 percent to owner
    survey.user.wallet += owner_total
    survey.user.save()

    # 70 percent to winners
    # total_price_except_winning_option * 0.7
    all_winners_votes = SurveyVote.objects.filter(survey_option=winning_option).all()
    users = []
    for vote in all_winners_votes:
        if vote.user not in users:
            vote.user.wallet += vote.amount * 0.7
            vote.user.save()
            users.append(vote.user)

    # options = SurveyOption.objects.filter(survey=survey).all()
    # total = []
    # for option in options:
    #     votes = SurveyVote.objects.filter(survey_option=option).all()
    #     total_price = 0
    #     for vote in votes:
    #         total_price += vote.amount
    #
    #     total.append({
    #         'option': option,
    #         'votes': len(votes),
    #         'total_price': total_price
    #     })
    #
    # sorted_data = sorted(total, key=lambda x: x['total_price'])
    # grouped_data = {key: list(group) for key, group in groupby(sorted_data, key=lambda x: x['total_price'])}
    # total_price = sum(item['total_price'] for item in total)
    # max_price_option = max(total, key=lambda x: x['total_price'])['option']
    #
    # print(f"Option с максимальной ценой: {max_price_option}")
    #
    # print(grouped_data)
    #
    # for price, items in grouped_data.items():
    #     percent_price = (price / total_price) * 100
    #     print(f"Price: {price}, Percentage of Total Price: {percent_price:.2f}%")


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

        survey_options = SurveyOption.objects.filter(survey=survey).all()
        if SurveyVote.objects.filter(survey_option__in=survey_options, user=request.user).exists():
            return Response({"message": "Vote is already added"}, status=status.HTTP_404_NOT_FOUND)

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

            if not 0.1 < amount < 1300:
                return Response({"message": "Amount must be greater than 0.1 and less than 1300"},
                                status=status.HTTP_404_NOT_FOUND)

            if request.user.wallet < amount:
                return Response({"message": "Not enough jetons to vote"}, status=status.HTTP_404_NOT_FOUND)

        # exists_survey_vote = SurveyVote.objects.filter(survey_option=survey_option, user=request.user,
        #                                                survey=survey).first()
        # if exists_survey_vote:
        #     return Response({"message": "Vote is already added"}, status=status.HTTP_404_NOT_FOUND)

        all_votes = SurveyVote.objects.filter(survey=survey).count()
        if survey.vote_limit and all_votes >= survey.vote_limit:
            submit_survey(survey=survey)
            return Response({"message": "Max votes reached"}, status=status.HTTP_404_NOT_FOUND)

        survey_vote = SurveyVote(survey_option=survey_option, user=request.user, survey=survey, amount=amount)
        survey_vote.save()

        serializer = SurveyVoteApiSerializer(survey_vote)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
