from rest_framework import serializers
from core.models import SearchRecord


class SearchRecordSerializer(serializers.ModelSerializer):
    searcher = serializers.StringRelatedField(read_only=True)
    class Meta:
        model = SearchRecord
        fields = '__all__'