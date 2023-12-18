from rest_framework import serializers
from ..models import Survey


class SurveyApiSerializer(serializers.ModelSerializer):
    view_count = serializers.SerializerMethodField(source='get_view_count', read_only=True)
    class Meta:
        model = Survey
        fields = '__all__'
