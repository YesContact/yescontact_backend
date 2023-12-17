from rest_framework import serializers
from ..models import Like


class SurveyLikeApiSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = '__all__'
