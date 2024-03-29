from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.fields import FileField, SerializerMethodField

from survey.serializers.survey_vote import SurveyVoteApiSerializer
from ..models import SurveyOption, Survey, SurveyVote


class SurveyOptionApiSerializer(serializers.ModelSerializer):
    # options = serializers.SerializerMethodField(source='get_options', read_only=True)
    my_vote = SerializerMethodField()
    votes_count = SerializerMethodField()

    def get_my_vote(self, obj):
        vote = SurveyVote.objects.filter(survey_option=obj, user=self.context.get('request').user).first()
        if not vote:
            return None
        serializer = SurveyVoteApiSerializer(vote, context={'request': self.context.get('request')})
        return serializer.data

    def get_votes_count(self, obj):
        return SurveyVote.objects.filter(survey_option=obj).count()

    class Meta:
        model = SurveyOption
        fields = '__all__'


class CreateSurveyOptionWithSurveyApiSerializer(serializers.ModelSerializer):
    image = Base64ImageField(required=True, allow_null=True)

    def validate_image(self, value):
        max_size = 4 * 1024 * 1024
        if not value:
            raise ValidationError("Provide option image")
        if value.size > max_size:
            raise ValidationError("Image size must be less than 4MB")
        return value

    class Meta:
        model = SurveyOption
        # fields = '__all__'
        exclude = ['survey']


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

    # def validate_image(self, value):
    #     survey_id = self.initial_data.get('paid')
    #
    #     # instance = Survey.objects.filter(id=survey_id).first()
    #     # if not instance:
    #     #     raise ValidationError('Survey with this id not found')
    #
    #     print(instance)
    #     print(instance.survey)
    #
    #     if instance.survey.paid:
    #         max_size = 1024 * 1024 * 4
    #         if value.size > max_size:
    #             raise ValidationError(f'Image size should be less than {max_size} mbytes')
    #     elif not instance.survey.paid:
    #         max_size = 1024 * 1024 * 2
    #         if value.size > max_size:
    #             raise ValidationError(f'Image size should be less than {max_size} mbytes')
    #     return value

    def create(self, validated_data):
        # user = self.context['request'].user
        survey_option = SurveyOption.objects.create(**validated_data)
        return survey_option


class SurveyOptionDetailApiSerializer(serializers.ModelSerializer):
    class Meta:
        model = SurveyOption
        fields = '__all__'
