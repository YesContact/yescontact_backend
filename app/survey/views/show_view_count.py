from drf_yasg.utils import swagger_auto_schema
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..models import Survey
from ..serializers import SurveyApiSerializer


class ShowViewCountApiView(APIView):
    serializer_class = SurveyApiSerializer

    def get(self, request):
        surveys = Survey.objects.all()
        serialized_data = self.serializer_class(surveys, many=True).data

        for survey_data in serialized_data:
            survey_id = survey_data['id']
            view_count = Survey.objects.get(id=survey_id).view_count
            survey_data['view_count'] = view_count

        return Response(serialized_data, status=status.HTTP_200_OK)
    

    @swagger_auto_schema(
        responses={200: SurveyApiSerializer(many=True)}
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)