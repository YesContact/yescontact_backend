from rest_framework import serializers

from users.models import CustomUser
from survey.models.survey import Survey


class SurveyUserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'full_name', 'phone_number', 'email', 'username', 'description']


class SurveyUserListSerializer(serializers.ModelSerializer):
    survey_count = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'full_name', 'phone_number', 'email', 'created_at', 'username',
                  'survey_count', 'description']

    def get_survey_count(self, obj):
        return Survey.objects.filter(user=obj).count()


class SurveyUserDetailSerializer(serializers.ModelSerializer):
    survey_count = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'full_name', 'phone_number', 'email', 'username', 'description', 'survey_count']

    def to_representation(self, instance):
        request = self.context.get('request')

        if request and request.method == 'PUT' or request.method == 'PATCH':
            data = super().to_representation(instance)
            data.pop('survey_count', None)
            return data

        return super().to_representation(instance)

    def get_survey_count(self, obj):
        return Survey.objects.filter(user=obj).count()
