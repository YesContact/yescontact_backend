from rest_framework.generics import ListAPIView
from ..models import Survey
from ..serializers import SurveyApiSerializer


class SurveyApiView(ListAPIView):
    queryset = Survey.objects.all()
    serializer_class = SurveyApiSerializer
