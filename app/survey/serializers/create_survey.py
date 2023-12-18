from rest_framework import serializers
from ..models import Survey


class CreateSurveyApiSerializer(serializers.ModelSerializer):
    view_count = serializers.SerializerMethodField(source='get_view_count', read_only=True)
    class Meta:
        model = Survey
        fields = ['id', 'title', 'description', 'end_time', 'view_count', 'paid',]
