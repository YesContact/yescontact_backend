from django.db.models import Q
from django.utils.decorators import method_decorator
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.generics import ListAPIView
from ..models import Survey
from ..serializers import SurveyApiSerializer


class SurveyApiView(ListAPIView):
    queryset = Survey.objects.all()
    serializer_class = SurveyApiSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        survey_type = self.request.query_params.get('survey_type')

        filter_params = Q()
        if survey_type == 'paid':
            filter_params |= Q(paid=True)
        elif survey_type == 'free':
            filter_params |= Q(paid=False)
        else:
            filter_params |= Q()

        queryset = queryset.filter(filter_params)

        return queryset

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'survey_type',
                openapi.IN_QUERY,
                description="Surveys type (free, paid), If you want all don't specify this field",
                type=openapi.TYPE_STRING
            ),
        ],
        responses={200: SurveyApiSerializer(many=True)}
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
