from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from ..models import Survey, CommentLike, Comment
from ..serializers import SurveyCommentLikeApiSerializer


@extend_schema(
    parameters=[
        OpenApiParameter(name='comment_id', type=int, description='Specify id of comment to get all likes',
                         required=True),
    ],
    responses={200: SurveyCommentLikeApiSerializer(many=True)},
    tags=['Api Survey Comment Like']
)
class SurveyCommentLikeApiView(ListAPIView):
    queryset = CommentLike.objects.all()
    serializer_class = SurveyCommentLikeApiSerializer

    # def get_queryset(self):
    #     queryset = super().get_queryset()
    #     survey_id = self.request.query_params.get('comment_id')
    #     if not survey_id:
    #         raise ValidationError('Specify comment_id parameter')
    #
    #     exist_comment = Comment.objects.filter(id=survey_id)
    #     if not exist_comment.exists():
    #         raise ValidationError('Comment with this id not found')
    #
    #     queryset = queryset.filter(comment=exist_comment.first())
    #
    #     return queryset

    # @swagger_auto_schema(
    #     manual_parameters=[
    #         openapi.Parameter(
    #             'comment_id',
    #             openapi.IN_QUERY,
    #             description="Specify id of comment to get all likes",
    #             type=openapi.TYPE_INTEGER,
    #             required=True
    #         ),
    #     ],
    #     responses={200: SurveyCommentLikeApiSerializer(many=True)},
    #     tags=['Api Survey Comment Like']
    # )
    def get(self, request, *args, **kwargs):
        comment_id = self.request.query_params.get('comment_id')
        comment = Comment.objects.filter(id=comment_id).first()

        if not comment_id:
            raise ValidationError('Comment ID is missing in query parameters')

        if not comment:
            raise ValidationError('Comment with this id not found')

        queryset = CommentLike.objects.filter(comment=comment_id)
        count = queryset.count()

        response_data = {
            'count': count
        }

        return Response(response_data)
        # return super().get(request, *args, **kwargs)


@extend_schema(
    parameters=[
        OpenApiParameter(name='comment_id', type=int, description='Specify id of comment to add new like',
                         required=True),
    ],
    responses={200: SurveyCommentLikeApiSerializer},
    tags=['Api Survey Comment Like']
)
class CreateSurveyCommentLikeApiView(APIView):
    # @swagger_auto_schema(
    #     manual_parameters=[
    #         openapi.Parameter(
    #             'comment_id',
    #             openapi.IN_QUERY,
    #             description="Specify id of comment to add new like",
    #             type=openapi.TYPE_INTEGER,
    #             required=True
    #         ),
    #     ],
    #     responses={201: SurveyCommentLikeApiSerializer},
    #     tags=['Api Survey Comment Like']
    # )
    def post(self, request, *args, **kwargs):
        comment_id = self.request.query_params.get('comment_id')
        try:
            comment = Comment.objects.get(id=comment_id)
        except Survey.DoesNotExist:
            return Response({"message": "Comment not found"}, status=status.HTTP_404_NOT_FOUND)

        exists_comment_like = CommentLike.objects.filter(comment=comment, user=request.user).first()
        if exists_comment_like:
            return Response({"message": "Like is already added"}, status=status.HTTP_404_NOT_FOUND)

        comment_like = CommentLike(comment=comment, user=request.user)
        comment_like.save()

        serializer = SurveyCommentLikeApiSerializer(comment_like)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
