from rest_framework import serializers
from ..models import SurveyVote


class SurveyVoteApiSerializer(serializers.ModelSerializer):
    class Meta:
        model = SurveyVote
        fields = '__all__'
