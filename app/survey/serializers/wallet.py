from rest_framework import serializers


class WalletIncreaseSerializer(serializers.Serializer):
    amount = serializers.IntegerField()
