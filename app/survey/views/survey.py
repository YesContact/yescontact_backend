import json

from django.db.models import Q
from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.generics import ListAPIView, UpdateAPIView, CreateAPIView, RetrieveUpdateAPIView, RetrieveAPIView
from rest_framework.mixins import ListModelMixin
from rest_framework.parsers import MultiPartParser, JSONParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from users.models import CustomUser
from ..models import Survey, SurveyOption
from ..pagination import SurveyListPagination
from ..permissions import IsOwnerOrReadOnlyUser, IsVisibleSurvey
from ..serializers import SurveyApiSerializer, SurveyDetailSerializer, CreateFreeSurveyApiSerializer, \
    CreatePaidSurveyApiSerializer

from app.tasks import process_survey_start_time, process_survey_end_time


@extend_schema(
    parameters=[
        OpenApiParameter(name='survey_type', type=str,
                         description="Surveys type (free, paid), If you want all don't specify this field"),
        OpenApiParameter(name='user_id', type=str, description="Provide id of the creator of the survey"),
    ],
    responses={200: SurveyApiSerializer(many=True)},
    tags=['Api Survey'])
class SurveyApiView(ListAPIView, ListModelMixin):
    queryset = Survey.objects.filter(status='active')
    serializer_class = SurveyApiSerializer
    pagination_class = SurveyListPagination
    permission_classes = [IsAuthenticated, IsVisibleSurvey]

    def get_queryset(self):
        queryset = super().get_queryset()
        survey_type = self.request.query_params.get('survey_type')
        user_id = self.request.query_params.get('user_id')

        filter_params = Q()

        if user_id:
            user = CustomUser.objects.filter(id=user_id).first()
            if not user:
                raise ValidationError("User not found")
            filter_params &= Q(user=user)

        if survey_type == 'paid':
            filter_params &= Q(paid=True)
        elif survey_type == 'free':
            filter_params &= Q(paid=False)
        else:
            filter_params &= Q()
        queryset = queryset.filter(filter_params).order_by('-created_at')
        # print(queryset)

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
class SurveyDetailView(RetrieveAPIView):
    queryset = Survey.objects.all()
    # serializer_class = SurveyDetailSerializer
    serializer_class = SurveyApiSerializer
    permission_classes = [IsAuthenticated, IsVisibleSurvey]

    # def get_serializer_class(self):
    #     if self.request.method in ['PUT', 'PATCH']:
    #         return SurveyDetailSerializer
    #     else:
    #         return SurveyApiSerializer

    # @swagger_auto_schema(tags=['Api Survey'])
    # def update_survey(self, request, *args, **kwargs):
    #     survey_id = kwargs.get('pk')
    #
    #     try:
    #         survey = Survey.objects.get(pk=survey_id)
    #         # survey.update_start_time()
    #
    #         # active_status = request.data.get('active')
    #         end_time = request.data.get('end_time')
    #         # cost = request.data.get('cost')
    #
    #
    #         if end_time:
    #             status = survey.check_date_difference(end_time=end_time)
    #             if not status:
    #                 raise ValidationError('End date is smaller than Start date')
    #
    #         survey_options = SurveyOption.objects.filter(survey=survey).count()
    #         if survey_options < 2:
    #             raise ValidationError('Options for survey are less than the minimum 2')

            # if survey.paid:
            #     if not survey.cost and not cost:
            #         raise ValidationError('Cost specified is required')
            #
            #     if not 10 <= cost <= 3000:
            #         raise ValidationError('Cost must be between 10 and 3000')





        # except Survey.DoesNotExist:
        #     raise ValidationError('Survey not found')
        #
        # if request.method == 'PUT':
        #     return super().put(request, *args, **kwargs)
        # elif request.method == 'PATCH':
        #     return super().patch(request, *args, **kwargs)

    # put = update_survey
    # patch = update_survey

    # @swagger_auto_schema(tags=['Api Survey'])
    # def get(self, request, *args, **kwargs):
    #     return super().get(request, *args, **kwargs)


@extend_schema(
    request=CreateFreeSurveyApiSerializer,
    responses={200: CreateFreeSurveyApiSerializer(many=True)},
    tags=['Api Survey'])
class CreateFreeSurveyApiView(CreateAPIView):
    queryset = SurveyOption.objects.all()
    serializer_class = CreateFreeSurveyApiSerializer
    # parser_classes = [MultiPartParser, JSONParser]
    # parser_classes = [MultiPartParser]

    # def perform_create(self, serializer):
    #     options_data = self.request.data.get('options', [])
    #     if options_data > 15:
    #         raise ValidationError('Options for survey are more than the maximum 15')
    #
    #     survey = serializer.save()
    #
    #     for option_data in options_data:
    #         SurveyOption.objects.create(survey=survey, **option_data)

    # def post(self, request, *args, **kwargs):
    #     serializer = CreateFreeSurveyApiSerializer(data=request.data)
    #
    #     # Обработка данных JSON вручную
    #     options_data_str = request.data.get('options')
    #     if options_data_str:
    #         options_data = json.loads(options_data_str)
    #         updated_data = request.data.copy()
    #         updated_data['options'] = options_data
    #     else:
    #         updated_data = request.data
    #
    #     serializer = CreateFreeSurveyApiSerializer(data=updated_data)
    #     serializer.is_valid(raise_exception=True)
    #     serializer.save()
    #     return Response(serializer.data, status=status.HTTP_201_CREATED)


@extend_schema(tags=['Api Survey'])
class CreatePaidSurveyApiView(CreateAPIView):
    queryset = SurveyOption.objects.all()
    serializer_class = CreatePaidSurveyApiSerializer
    # parser_classes = [MultiPartParser]


@extend_schema(
    parameters=[
        OpenApiParameter(name='survey_id', type=int, description='Specify id of survey to start',
                         required=True, location='query'),
    ],
    responses={200: SurveyApiSerializer},
    tags=['Api Survey']
)
class StartSurveyApiView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        survey_id = request.GET.get('survey_id')
        survey = Survey.objects.filter(id=survey_id).first()
        if not survey:
            raise ValidationError('Survey not found')

        if survey.user != request.user:
            raise ValidationError('You are not the creator of this survey')

        if not survey.status == 'ready_to_start':
            raise ValidationError('Survey is not ready to start')

        if not survey.end_time:
            raise ValidationError('End date not specified')

        survey.update_start_time()
        status = survey.check_date_difference(end_time=survey.end_time)
        if not status:
            raise ValidationError('End date is smaller than Start date')

        if survey.paid:
            if not survey.cost:
                raise ValidationError('Cost specified is required')
            if not 10 <= survey.cost <= 3000:
                raise ValidationError('Cost must be between 10 and 3000')

        if survey.cost > request.user.wallet:
            raise ValidationError('Insufficient balance')
        
        process_survey_start_time.apply_async(args=[survey_id], countdown=survey.start_time.seconds_until_start())
        process_survey_end_time.apply_async(args=[survey_id], countdown=survey.end_time.seconds_until_end())

        return Response({"message": "POST request processed"}, status=status.HTTP_200_OK)
