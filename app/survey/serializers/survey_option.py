from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.fields import FileField

from ..models import SurveyOption, Survey


class SurveyOptionApiSerializer(serializers.ModelSerializer):
    # options = serializers.SerializerMethodField(source='get_options', read_only=True)
    class Meta:
        model = SurveyOption
        fields = '__all__'


class CreateSurveyOptionApiSerializer(serializers.ModelSerializer):
    class Meta:
        model = SurveyOption
        fields = '__all__'

    def validate(self, data):
        survey = data.get('survey')
        survey_options = SurveyOption.objects.filter(survey=survey).count()
        if survey_options >= 15:
            raise ValidationError('Limit 15 Survey Options')

        return data

    def create(self, validated_data):
        # user = self.context['request'].user
        survey_option = SurveyOption.objects.create(**validated_data)
        return survey_option

