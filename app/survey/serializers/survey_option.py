from rest_framework import serializers
from ..models import SurveyOption


class SurveyOptionApiSerializer(serializers.ModelSerializer):
    options = serializers.SerializerMethodField(source='get_options', read_only=True)
    class Meta:
        model = SurveyOption
        fields = '__all__'
