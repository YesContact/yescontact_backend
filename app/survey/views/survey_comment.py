from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.exceptions import ValidationError
from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.permissions import IsAuthenticated

from ..models import Survey, Comment
from ..serializers import CreateSurveyCommentApiSerializer, CommentTreeSerializer


@extend_schema(
    parameters=[
        OpenApiParameter(name='survey_id', type=int, description='Specify id of survey to get all comments',
                         required=True),
    ],
    responses={200: CommentTreeSerializer(many=True)},
    tags=['Api Survey Comment']
)
class SurveyCommentApiView(ListAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentTreeSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        survey_id = self.request.query_params.get('survey_id')
        if not survey_id:
            raise ValidationError('Specify survey_id parameter')

        exist_survey = Survey.objects.filter(id=survey_id)
        if not exist_survey.exists():
            raise ValidationError('Survey with this id not found')

        queryset = queryset.filter(survey=exist_survey.first(), parent_comment=None)

        return queryset

    # @swagger_auto_schema(
    #     manual_parameters=[
    #         openapi.Parameter(
    #             'survey_id',
    #             openapi.IN_QUERY,
    #             description="Specify id of survey to get all comments",
    #             type=openapi.TYPE_INTEGER,
    #             required=True
    #         ),
    #     ],
    #     responses={200: CommentTreeSerializer(many=True)},
    #     tags=['Api Survey Comment']
    # )
    # def get(self, request, *args, **kwargs):
    #     return super().get(request, *args, **kwargs)


@extend_schema(tags=['Api Survey Comment'])
class SurveyCommentCreateAPIView(CreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CreateSurveyCommentApiSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    # @swagger_auto_schema(tags=['Api Survey Comment'])
    # def post(self, request, *args, **kwargs):
    #     return super().post(request, *args, **kwargs)
