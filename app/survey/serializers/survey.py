from django.db import transaction
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.fields import SerializerMethodField

from survey.serializers.survey_option import CreateSurveyOptionApiSerializer, CreateSurveyOptionWithSurveyApiSerializer
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
        exclude = ["view_count"]
        # fields = '__all__'


class SurveyDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Survey
        # exclude = ['user', 'survey_id', 'view_count', 'start_time', 'cost']
        fields = ["title", "description", "end_time", "vote_limit"]

    def validate_cost(self, value):
        if not 10 <= value <= 3000:
            raise serializers.ValidationError("Cost must be between 10 and 3000")
        return value


class CreateFreeSurveyApiSerializer(serializers.ModelSerializer):
    title = serializers.CharField(max_length=100)
    description = serializers.CharField(max_length=1000)
    end_time = serializers.DateTimeField()
    # image = serializers.ImageField()
    image = Base64ImageField(required=False, allow_null=True)
    options = CreateSurveyOptionWithSurveyApiSerializer(many=True, write_only=True)

    # paid = serializers.BooleanField()

    # options = serializers.ListField(child=serializers.CharField(max_length=100), min_length=2, max_length=15)
    class Meta:
        model = Survey
        fields = [
            "id",
            "title",
            "image",
            "description",
            "end_time",
            "vote_limit",
            "options",
            "visibility",
            # "view_count",
        ]

    def validate_image(self, value):
        max_size = 2 * 1024 * 1024
        if value.size > max_size:
            raise ValidationError("Image size must be less than 2MB")
        return value

    @transaction.atomic
    def create(self, validated_data):
        user = self.context["request"].user
        cost = 0
        # options = self.validated_data.get('options')

        options_data = validated_data.pop('options', None)

        survey = Survey.objects.create(user=user, cost=cost, **validated_data)
        if options_data:
            for option_data in options_data:
                SurveyOption.objects.create(survey=survey, **option_data)

        # for option in options:
        #     print(option)

        return survey


class CreatePaidSurveyApiSerializer(serializers.ModelSerializer):
    title = serializers.CharField(max_length=100)
    description = serializers.CharField(max_length=1000)
    start_time = serializers.DateTimeField()
    end_time = serializers.DateTimeField()
    # image = serializers.ImageField()
    image = Base64ImageField(required=False, allow_null=True)
    options = CreateSurveyOptionWithSurveyApiSerializer(many=True, write_only=True)
    # options = serializers.SerializerMethodField()

    # paid = serializers.BooleanField()

    # options = serializers.ListField(child=serializers.CharField(max_length=100), min_length=2, max_length=15)
    class Meta:
        model = Survey
        fields = [
            "id",
            "title",
            "description",
            "start_time",
            "end_time",
            "vote_limit",
            "cost",
            "visibility",
            "image",
            "options",
            # "view_count",

        ]

    def validate_image(self, value):
        max_size = 4 * 1024 * 1024
        if value.size > max_size:
            raise ValidationError("Image size must be less than 4MB")
        return value

    def validate_cost(self, value):
        if value is None:
            raise ValidationError("Cost is required.")
        if not 10 <= value <= 3000:
            raise ValidationError("Cost must be between 10 and 3000.")

        return value
    
    def validate_end_time(self, value):
        cost = self.initial_data.get('cost')
        start_time = self.initial_data.get('start_time')
        end_time = self.initial_data.get('end_time')

        if cost is not None and (start_time is None or end_time is None):
            raise ValidationError("Start time and end time are required for paid surveys.")
        
        if start_time and end_time and start_time >= end_time:
            raise ValidationError("End time must be greater than start time.") 

        return value

    # def get_options(self, obj):
    #     survey_options = SurveyOption.objects.filter(survey=obj).all()
    #     return CreateSurveyOptionWithSurveyApiSerializer(survey_options, many=True).data

    # def create(self, validated_data):
    #     user = self.context["request"].user
    #     paid = True
    #     survey = Survey.objects.create(user=user, paid=paid, **validated_data)
    #     return survey
    @transaction.atomic
    def create(self, validated_data):
        user = self.context["request"].user
        paid = True
        # options = self.validated_data.get('options')

        options_data = validated_data.pop('options', None)
        test = validated_data
        survey = Survey.objects.create(user=user, paid=paid, **validated_data)
        if options_data:
            for option_data in options_data:
                SurveyOption.objects.create(survey=survey, **option_data)

        # for option in options:
        #     print(option)

        return survey
