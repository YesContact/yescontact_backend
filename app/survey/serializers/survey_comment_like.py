from rest_framework import serializers
from ..models import CommentLike


class SurveyCommentLikeApiSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommentLike
        fields = '__all__'
