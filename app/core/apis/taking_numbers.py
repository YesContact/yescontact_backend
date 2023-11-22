from rest_framework import status
from rest_framework.response import Response
from rest_framework import viewsets
from core.models import Contact
from core.serializers import ContactSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework import viewsets
from core.models import Contact
from core.serializers import ContactSerializer
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema


class TakingNumbersViewSet(viewsets.ModelViewSet):
    serializer_class = ContactSerializer

    @swagger_auto_schema(manual_parameters=[
        openapi.Parameter('user_id', in_=openapi.IN_QUERY, type=openapi.TYPE_INTEGER)
    ])

    def list(self, request, *args, **kwargs):
        user_id = request.query_params.get('user_id', None)
        if user_id:
            try:
                user_id = int(user_id)  # Convert to integer
                if not Contact.objects.filter(user_id=user_id).exists():
                    return Response({'message': f"User with ID {user_id} does not exist"},
                                    status=status.HTTP_400_BAD_REQUEST)
                queryset = Contact.objects.filter(user_id=user_id)
            except ValueError:
                return Response({'message': 'Invalid user_id provided'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'message': 'user_id is required'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = ContactSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = ContactSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(
            serializer.errors, status=status.HTTP_400_BAD_REQUEST
        )

