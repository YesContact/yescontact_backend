from rest_framework import serializers

from users.models import CustomUser


class SurveyUserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'full_name', 'phone_number', 'email', 'username']
        # fields = '__all__'
        # fields = '__all__'


class SurveyUserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'full_name', 'phone_number', 'email', 'created_at', 'username', 'survey_count']
        # exclude = ['otp', 'password', 'password_confirm', '']


class SurveyUserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'full_name', 'phone_number', 'email', 'username']
