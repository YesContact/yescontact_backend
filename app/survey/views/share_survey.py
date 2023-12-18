from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import secrets
from django.urls import reverse
from ..models import Survey
from ..serializers import ShareSurveyApiSerializer


class ShareSurveyAPIView(APIView):
    serializer_class = ShareSurveyApiSerializer

    @swagger_auto_schema(
        request_body=ShareSurveyApiSerializer, responses={200: ShareSurveyApiSerializer}
    )
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            survey_id = serializer.validated_data["survey_id"]
            try:
                survey = Survey.objects.get(id=survey_id)
                survey.shared = True

                unique_token = secrets.token_urlsafe(16)

                survey.unique_link_token = unique_token
                survey.save()

                unique_link = request.build_absolute_uri(
                    reverse("survey-detail", kwargs={"token": unique_token})
                )

                return Response({"unique_link": unique_link}, status=status.HTTP_200_OK)
            except Survey.DoesNotExist:
                return Response(
                    {"message": f"Survey with ID {survey_id} does not exist."},
                    status=status.HTTP_404_NOT_FOUND,
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
