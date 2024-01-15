from drf_spectacular.utils import extend_schema
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from survey.serializers import JetonConverterSerializer


@extend_schema(tags=['Api Jeton'])
class JetonConverterView(generics.CreateAPIView):
    serializer_class = JetonConverterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        number_to_multiply = serializer.validated_data['dollar']

        MULTIPLIER_CONSTANT = 10

        result = number_to_multiply * MULTIPLIER_CONSTANT

        return Response({"jeton": result}, status=status.HTTP_200_OK)