from rest_framework import serializers
from ..models import SurveyView


class SurveyViewApiSerializer(serializers.ModelSerializer):
    class Meta:
        model = SurveyView
        fields = '__all__'


