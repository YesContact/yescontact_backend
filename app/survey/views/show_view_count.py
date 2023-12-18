from drf_yasg.utils import swagger_auto_schema
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db import models
from rest_framework import status
from ..models import Survey
from ..serializers import ShowViewCountSerializer


class ShowViewCountApiView(APIView):
    serializer_class = ShowViewCountSerializer

    @swagger_auto_schema(
        responses={200: ShowViewCountSerializer(many=True)}
    )
    def get(self, request):
        surveys = Survey.objects.all()
        serialized_data = self.serializer_class(surveys, many=True).data

        survey_ids = [survey_data['id'] for survey_data in serialized_data]

        view_counts = Survey.objects.filter(id__in=survey_ids).values('id').annotate(view_count=models.Count('views'))

        view_count_dict = {view['id']: view['view_count'] for view in view_counts}

        for survey_data in serialized_data:
            survey_id = survey_data['id']
            survey_data['view_count'] = view_count_dict.get(survey_id, 0)

        return Response(serialized_data, status=status.HTTP_200_OK)
    