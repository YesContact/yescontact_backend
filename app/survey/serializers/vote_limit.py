from rest_framework import serializers
from ..models import SurveyOption

class VoteLimitSerializer(serializers.Serializer):
    survey_id = serializers.IntegerField()
    voice_limit = serializers.IntegerField()

    class Meta:
        model = SurveyOption
        fields = ['survey_id', 'voice_limit']
