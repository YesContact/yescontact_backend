from rest_framework import serializers
from ..models import Survey


class SurveyApiSerializer(serializers.ModelSerializer):
    class Meta:
        model = Survey
        fields = '__all__'