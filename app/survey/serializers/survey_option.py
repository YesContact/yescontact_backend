from rest_framework import serializers
from ..models import SurveyOption


class SurveyOptionApiSerializer(serializers.ModelSerializer):
    class Meta:
        model = SurveyOption
        fields = '__all__'
