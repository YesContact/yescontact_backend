from django.db import transaction
from django.db.models import Count
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.fields import SerializerMethodField

from survey.serializers.survey_option import CreateSurveyOptionApiSerializer, CreateSurveyOptionWithSurveyApiSerializer
from ..models import Survey, SurveyOption, SurveyView, SurveyVote
from app.tasks import process_survey_start_time, process_survey_end_time


class SurveyApiSerializer(serializers.ModelSerializer):
    # view_count = serializers.SerializerMethodField(source='get_view_count', read_only=True)
    options = SerializerMethodField()
    views_count = serializers.SerializerMethodField()
    stats = serializers.SerializerMethodField()

    def get_options(self, obj):
        from . import SurveyOptionApiSerializer

        options = SurveyOption.objects.filter(survey=obj).all()
        serializer = SurveyOptionApiSerializer(options, many=True)
        return serializer.data

    def get_views_count(self, obj):
        return SurveyView.objects.filter(survey=obj).count()

    def get_stats(self, obj: Survey):
        if obj.check_completed:
            all_options = SurveyOption.objects.filter(survey=obj).all()
            votes_count_per_option = SurveyVote.objects.filter(
                survey_option__in=all_options).values('survey_option').annotate(
                count=Count('id'))
            total_votes = SurveyVote.objects.filter(survey_option__in=all_options).count()

            result_array = [{'option_id': vote.get('survey_option'),
                             'percentage': (vote.get('count') / total_votes) * 100} for vote in
                            votes_count_per_option]
            return result_array
        else:
            return None


    class Meta:
        model = Survey
        exclude = ["view_count"]
        # fields = '__all__'


class SurveyDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Survey
        # exclude = ['user', 'survey_id', 'view_count', 'start_time', 'cost']
        fields = ["title", "description", "end_time", "vote_limit"]

    # def validate_cost(self, value):
    #     if not 10 <= value <= 3000:
    #         raise serializers.ValidationError("Cost must be between 10 and 3000")
    #     return value


class CreateFreeSurveyApiSerializer(serializers.ModelSerializer):
    title = serializers.CharField(max_length=100)
    description = serializers.CharField(max_length=1000)
    end_time = serializers.DateTimeField()
    # image = serializers.ImageField()
    image = Base64ImageField(required=False, allow_null=True)
    options = CreateSurveyOptionWithSurveyApiSerializer(many=True, write_only=True)

    FILE_MAX_SIZE = 2 * 1024 * 1024

    class Meta:
        model = Survey
        fields = [
            "id",
            "title",
            "description",
            "end_time",
            "vote_limit",
            "visibility",
            "image",
            "options",
            "visibility",
        ]

    def validate_image(self, value):
        if value:
            if value.size > self.FILE_MAX_SIZE:
                raise ValidationError("Image size must be less than 2MB")
        return value

    @transaction.atomic
    def create(self, validated_data):
        user = self.context["request"].user
        cost = 0
        # options = self.validated_data.get('options')

        options_data = validated_data.pop('options', None)
        if not 2 <= len(options_data) <= 15:
            raise ValidationError("Options count must be between 2 and 15")

        survey = Survey.objects.create(user=user, cost=cost, **validated_data)
        if options_data:
            for option_data in options_data:
                if option_data.get('image', None):
                    if option_data.get('image').size > self.FILE_MAX_SIZE:
                        raise ValidationError("Image size of option must be less than 2MB")

                SurveyOption.objects.create(survey=survey, **option_data)

        # for option in options:
        #     print(option)

        # process_survey_start_time.apply_async(args=[survey.id], countdown=survey.start_time.seconds_until_start())
        # process_survey_end_time.apply_async(args=[survey.id], countdown=survey.end_time.seconds_until_end())

        return survey


class CreatePaidSurveyApiSerializer(serializers.ModelSerializer):
    title = serializers.CharField(max_length=100)
    description = serializers.CharField(max_length=1000)
    start_time = serializers.DateTimeField()
    end_time = serializers.DateTimeField()
    # image = serializers.ImageField()
    image = Base64ImageField(required=False, allow_null=True)
    options = CreateSurveyOptionWithSurveyApiSerializer(many=True, write_only=True)

    FILE_MAX_SIZE = 4 * 1024 * 1024

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
            "visibility",

        ]

    def validate_image(self, value):
        max_size = 4 * 1024 * 1024
        if not value:
            return value
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

    @transaction.atomic
    def create(self, validated_data):
        user = self.context["request"].user
        paid = True
        # options = self.validated_data.get('options')

        options_data = validated_data.pop('options', None)
        if not 2 <= len(options_data) <= 15:
            raise ValidationError("Options count must be between 2 and 15")
        survey = Survey.objects.create(user=user, paid=paid, **validated_data)
        if options_data:
            for option_data in options_data:
                if option_data.get('image', None):
                    if option_data.get('image').size > self.FILE_MAX_SIZE:
                        raise ValidationError("Image size of option must be less than 4MB")
                SurveyOption.objects.create(survey=survey, **option_data)

        if user.wallet < survey.cost:
            raise ValidationError("Insufficient balance.")

        user.wallet -= survey.cost
        user.save()

        survey.payment = True
        survey.save()

        survey.status = 'active'
        survey.save()



        # for option in options:
        #     print(option)

        return survey
