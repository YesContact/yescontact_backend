from drf_yasg.utils import swagger_auto_schema
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..models import Survey
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
            voice_limit = serializer.validated_data['voice_limit']

            try:
                survey = Survey.objects.get(id=survey_id)
                survey.voice_limit = voice_limit
                survey.save()
                
                return Response({'message': f"Vote limit for survey {survey_id} has been set to {voice_limit}."},
                                status=status.HTTP_200_OK)
            except Survey.DoesNotExist:
                return Response({'message': f"Survey with ID {survey_id} does not exist."},
                                status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
