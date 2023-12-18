from drf_yasg.utils import swagger_auto_schema
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..models import Survey, SurveyVote
from ..serializers import VoteLimitSerializer

class SetVoteLimitAPIView(APIView):
    serializer_class = VoteLimitSerializer


    @swagger_auto_schema(
        request_body=VoteLimitSerializer,
        responses={200: VoteLimitSerializer}
    )
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            survey_id = serializer.validated_data['survey_id']
            vote_limit = serializer.validated_data['vote_limit']

            try:
                survey = SurveyVote.objects.get(id=survey_id)
                survey.survey_option.survey.vote_limit = vote_limit
                survey.save()
                
                return Response({'message': f"Vote limit for survey {survey_id} has been set to {vote_limit}."},
                                status=status.HTTP_200_OK)
            except SurveyVote.DoesNotExist:
                return Response({'message': f"Survey with ID {survey_id} does not exist."},
                                status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
