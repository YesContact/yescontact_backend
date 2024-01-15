from django.db.models import Q
from drf_spectacular.utils import extend_schema
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.exceptions import ValidationError
from rest_framework.generics import ListAPIView, UpdateAPIView, CreateAPIView, RetrieveUpdateAPIView
from rest_framework.response import Response

from ..models import Survey, SurveyOption
from ..serializers import SurveyApiSerializer, SurveyDetailSerializer, CreateFreeSurveyApiSerializer, CreatePaidSurveyApiSerializer


@extend_schema(tags=['Api Survey'])
class SurveyApiView(ListAPIView):
    queryset = Survey.objects.filter(active=True)
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

    # @swagger_auto_schema(
    #     manual_parameters=[
    #         openapi.Parameter(
    #             'survey_type',
    #             openapi.IN_QUERY,
    #             description="Surveys type (free, paid), If you want all don't specify this field",
    #             type=openapi.TYPE_STRING
    #         ),
    #     ],
    #     responses={200: SurveyApiSerializer(many=True)},
    #     tags=['Api Survey']
    # )
    # def get(self, request, *args, **kwargs):
    #     return super().get(request, *args, **kwargs)


@extend_schema(tags=['Api Survey'])
class SurveyDetailView(RetrieveUpdateAPIView):
    queryset = Survey.objects.all()
    serializer_class = SurveyDetailSerializer

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return SurveyDetailSerializer
        else:
            return SurveyApiSerializer

    # @swagger_auto_schema(tags=['Api Survey'])
    def update_survey(self, request, *args, **kwargs):
        survey_id = kwargs.get('pk')

        try:
            survey = Survey.objects.get(pk=survey_id)
            survey.update_start_time()

            active_status = request.data.get('active')
            end_time = request.data.get('end_time')
            cost = request.data.get('cost')

            if active_status or survey.active:
                if end_time:
                    status = survey.check_date_difference(end_time=end_time)
                    if not status:
                        raise ValidationError('End date is smaller than Start date')

                survey_options = SurveyOption.objects.filter(survey=survey).count()
                if survey_options < 2:
                    raise ValidationError('Options for survey are less than the minimum 2')

                if not survey.cost and not cost:
                    raise ValidationError('Cost specified is required')

                if not 10 <= cost <= 3000:
                    raise ValidationError('Cost must be between 10 and 3000')





        except Survey.DoesNotExist:
            raise ValidationError('Survey not found')

        if request.method == 'PUT':
            return super().put(request, *args, **kwargs)
        elif request.method == 'PATCH':
            return super().patch(request, *args, **kwargs)

    put = update_survey
    patch = update_survey

    # @swagger_auto_schema(tags=['Api Survey'])
    # def get(self, request, *args, **kwargs):
    #     return super().get(request, *args, **kwargs)


@extend_schema(tags=['Api Survey'])
class CreateFreeSurveyApiView(CreateAPIView):
    queryset = SurveyOption.objects.all()
    serializer_class = CreateFreeSurveyApiSerializer


@extend_schema(tags=['Api Survey'])
class CreatePaidSurveyApiView(CreateAPIView):
    queryset = SurveyOption.objects.all()
    serializer_class = CreatePaidSurveyApiSerializer

    # @swagger_auto_schema(
    #     request_body=CreateSurveyApiSerializer,
    #     responses={200: CreateSurveyApiSerializer},
    #     tags=['Api Survey']
    # )
    # def post(self, request, *args, **kwargs):
    # serializer = self.get_serializer(data=request.data)
    # serializer.is_valid(raise_exception=True)
    # serializer.save()

    # new_survey = serializer.save(
    #     deadline=timezone.now() + timedelta(days=1)
    # )

    # expire_survey.apply_async((new_survey.id,), eta=new_survey.deadline)
    # return super().post(request, *args, **kwargs)
