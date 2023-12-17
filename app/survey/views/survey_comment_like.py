from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.exceptions import ValidationError
from rest_framework.generics import ListAPIView

from ..models import Survey, CommentLike, Comment
from ..serializers import SurveyCommentLikeApiSerializer


class SurveyCommentLikeApiView(ListAPIView):
    queryset = CommentLike.objects.all()
    serializer_class = SurveyCommentLikeApiSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        survey_id = self.request.query_params.get('comment_id')
        if not survey_id:
            raise ValidationError('Specify comment_id parameter')

        exist_comment = Comment.objects.filter(id=survey_id)
        if not exist_comment.exists():
            raise ValidationError('Comment with this id not found')

        queryset = queryset.filter(comment=exist_comment.first())

        return queryset

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'comment_id',
                openapi.IN_QUERY,
                description="Specify id of comment to get all likes",
                type=openapi.TYPE_INTEGER,
                required=True
            ),
        ],
        responses={200: SurveyCommentLikeApiSerializer(many=True)}
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
