from rest_framework import serializers
from ..models import Survey, SurveyOption
from .survey_option import SurveyOptionApiSerializer

class CreateSurveyApiSerializer(serializers.ModelSerializer):
    title = serializers.CharField(max_length=100)
    description = serializers.CharField(max_length=1000)
    end_time = serializers.DateTimeField()
    paid = serializers.BooleanField()
    options = serializers.ListField(child=serializers.CharField(max_length=100), min_length=2, max_length=15)
    class Meta:
        model = Survey
        fields = ['id', 'title', 'description', 'end_time', 'view_count', 'paid', 'options']


    def validate_options(self, options):
        if len(options) < 2:
            raise serializers.ValidationError("Survey must have at least 2 options.")
        if len(options) > 15:
            raise serializers.ValidationError("Survey can have at most 15 options.")
        return options

    def create(self, validated_data):
        options_data = validated_data.pop('options')
        survey = Survey.objects.create(**validated_data)
        
        for option_data in options_data:
            SurveyOption.objects.create(survey=survey, **option_data)

        return survey