from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.fields import SerializerMethodField

from survey.serializers.survey_option import CreateSurveyOptionApiSerializer
from ..models import Survey, SurveyOption, SurveyView


class SurveyApiSerializer(serializers.ModelSerializer):
    # view_count = serializers.SerializerMethodField(source='get_view_count', read_only=True)
    options = SerializerMethodField()
    views_count = serializers.SerializerMethodField()

    def get_options(self, obj):
        from . import SurveyOptionApiSerializer
        options = SurveyOption.objects.filter(survey=obj).all()
        serializer = SurveyOptionApiSerializer(options, many=True)
        return serializer.data

    def get_views_count(self, obj):
        return SurveyView.objects.filter(survey=obj).count()

    class Meta:
        model = Survey
        exclude = ['view_count']
        # fields = '__all__'


class SurveyDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Survey
        # exclude = ['user', 'survey_id', 'view_count', 'start_time', 'cost']
        fields = ['title', 'description', 'end_time', 'vote_limit']

    def validate_cost(self, value):
        if not 10 <= value <= 3000:
            raise serializers.ValidationError("Cost must be between 10 and 3000")
        return value


class CreateFreeSurveyApiSerializer(serializers.ModelSerializer):
    title = serializers.CharField(max_length=100)
    description = serializers.CharField(max_length=1000)
    end_time = serializers.DateTimeField()

    options = CreateSurveyOptionApiSerializer(many=True, write_only=True)

    # paid = serializers.BooleanField()

    # options = serializers.ListField(child=serializers.CharField(max_length=100), min_length=2, max_length=15)
    class Meta:
        model = Survey
        fields = ['id', 'title', 'description', 'end_time', 'vote_limit', 'options']

    def create(self, validated_data):
        user = self.context['request'].user
        cost = 0
        survey = Survey.objects.create(user=user, cost=cost, **validated_data)
        return survey


class CreatePaidSurveyApiSerializer(serializers.ModelSerializer):
    title = serializers.CharField(max_length=100)
    description = serializers.CharField(max_length=1000)
    end_time = serializers.DateTimeField()

    options = CreateSurveyOptionApiSerializer(many=True, write_only=True)

    # paid = serializers.BooleanField()

    # options = serializers.ListField(child=serializers.CharField(max_length=100), min_length=2, max_length=15)
    class Meta:
        model = Survey
        fields = ['id', 'title', 'description', 'end_time', 'vote_limit', 'cost', 'options']

    def validate_cost(self, value):
        if value is None:
            raise ValidationError("Cost is required.")
        if not 10 <= value <= 3000:
            raise ValidationError("Cost must be between 10 and 3000.")

        return value


    def create(self, validated_data):
        user = self.context['request'].user
        paid = True
        survey = Survey.objects.create(user=user, paid=paid, **validated_data)
        return survey
