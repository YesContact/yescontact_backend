from rest_framework import serializers
from ..models import Survey


class ShareSurveyApiSerializer(serializers.ModelSerializer):
    class Meta:
        model = Survey
        fields = ['id', 'title', 'description', 'paid', 'view_count']
