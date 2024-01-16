from drf_spectacular.utils import extend_schema, OpenApiResponse
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from survey.serializers import WalletIncreaseSerializer, JetonConverterSerializer


@extend_schema(
        responses={
            200: OpenApiResponse(response={"description": "Success", "example": {"jeton": "10000"}},
                                 description="Success"),
        },
        tags=['Api Wallet']
    )
class WalletIncreaseView(generics.CreateAPIView):
    serializer_class = WalletIncreaseSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        amount = serializer.validated_data['amount']

        MULTIPLIER_CONSTANT = 10

        result = amount * MULTIPLIER_CONSTANT
        total_result = result - (result * 0.03)
        request.user.wallet += total_result
        request.user.save()

        return Response({"jeton": total_result}, status=status.HTTP_200_OK)


@extend_schema(
        responses={
            200: OpenApiResponse(response={"description": "Success", "example": {"jeton": "10000",
                                                                                 "our_commission": "1%",
                                                                                 "company_commission": "2",
                                                                                 "total": "9900"}},
                                 description="Success"),
        },
        tags=['Api Wallet']
    )
class JetonConverterView(generics.CreateAPIView):
    serializer_class = JetonConverterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        number_to_multiply = serializer.validated_data['dollar']

        MULTIPLIER_CONSTANT = 10

        result = number_to_multiply * MULTIPLIER_CONSTANT

        data = {
            "jeton": result,
            "our_commission": "1%",
            "company_commission": "2%",
            "total": result - (result * 0.03)
        }

        return Response(data, status=status.HTTP_200_OK)

    # @extend_schema(
    #     responses={
    #         200: OpenApiResponse(response={"jeton": "10000", "our_commission": "1%", "company_commission": "2%",
    #                                        "total": "9900"}, description="Success"),
    #     },
    #     tags=['Api Wallet']
    # )
    # @extend_schema(
    #     responses={
    #         200: OpenApiResponse(response={"description": "Success", "example": {"message": "Logout Successfully",
    #                                                                              "code": 200}}, description="Success"),
    #     }
    # )
    # def get(self):
    #     pass
