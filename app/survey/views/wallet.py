from drf_spectacular.utils import extend_schema
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from survey.serializers import WalletIncreaseSerializer


@extend_schema(tags=['Api Wallet'])
class WalletIncreaseView(generics.CreateAPIView):
    serializer_class = WalletIncreaseSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        amount = serializer.validated_data['amount']

        # MULTIPLIER_CONSTANT = 10

        # result = number_to_multiply * MULTIPLIER_CONSTANT

        # return Response({"jeton": result}, status=status.HTTP_200_OK)