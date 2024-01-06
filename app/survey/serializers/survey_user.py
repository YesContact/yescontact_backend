from rest_framework import serializers

from users.models import CustomUser
from survey.models.survey import Survey
from survey.models.survey_vote import SurveyVote


class SurveyUserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'full_name', 'phone_number', 'email', 'username', 'description']


class SurveyUserListSerializer(serializers.ModelSerializer):
    survey_count = serializers.SerializerMethodField()
    vote_count = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'full_name', 'phone_number', 'email', 'created_at', 'username', 'description',
                  'survey_count', 'vote_count']

    def get_survey_count(self, obj):
        return Survey.objects.filter(user=obj).count()

    def get_vote_count(self, obj):
        return SurveyVote.objects.filter(user=obj).count()


class SurveyUserDetailSerializer(serializers.ModelSerializer):
    survey_count = serializers.SerializerMethodField()
    vote_count = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'full_name', 'phone_number', 'email', 'username', 'description', 'survey_count', 'vote_count']

    def to_representation(self, instance):
        request = self.context.get('request')

        if request and request.method == 'PUT' or request.method == 'PATCH':
            data = super().to_representation(instance)
            data.pop('survey_count', None)
            data.pop('vote_count', None)
            return data

        return super().to_representation(instance)

    def get_survey_count(self, obj):
        return Survey.objects.filter(user=obj).count()

    def get_vote_count(self, obj):
        return SurveyVote.objects.filter(user=obj).count()
