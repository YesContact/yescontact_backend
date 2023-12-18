from rest_framework import serializers
from ..models import Survey

class ShowViewCountSerializer(serializers.Serializer):
    survey_id = serializers.IntegerField()
    view_count = serializers.IntegerField()

    class Meta:
        model = Survey
        fields = {'survey_id', 'view_count'}
