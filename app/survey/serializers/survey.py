from rest_framework import serializers
from ..models import Survey


class SurveyApiSerializer(serializers.ModelSerializer):
    # view_count = serializers.SerializerMethodField(source='get_view_count', read_only=True)

    class Meta:
        model = Survey
        fields = '__all__'


class SurveyDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Survey
        exclude = ['user', 'survey_id', 'view_count', 'start_time']


class CreateSurveyApiSerializer(serializers.ModelSerializer):
    title = serializers.CharField(max_length=100)
    description = serializers.CharField(max_length=1000)
    end_time = serializers.DateTimeField()
    paid = serializers.BooleanField()

    # options = serializers.ListField(child=serializers.CharField(max_length=100), min_length=2, max_length=15)
    class Meta:
        model = Survey
        fields = ['id', 'title', 'description', 'end_time', 'paid', 'vote_limit']

    # def validate_options(self, options):
    #     if len(options) < 2:
    #         raise serializers.ValidationError("Survey must have at least 2 options.")
    #     if len(options) > 15:
    #         raise serializers.ValidationError("Survey can have at most 15 options.")
    #     return options



    def create(self, validated_data):
        # options_data = validated_data.pop('options')
        user = self.context['request'].user
        survey = Survey.objects.create(user=user, **validated_data)

        # for option_data in options_data:
        #     SurveyOption.objects.create(survey=survey, **option_data)

        return survey
