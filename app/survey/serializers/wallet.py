from rest_framework import serializers


class WalletIncreaseSerializer(serializers.Serializer):
    dollar = serializers.IntegerField()

class JetonConverterSerializer(serializers.Serializer):
    dollar = serializers.IntegerField()
