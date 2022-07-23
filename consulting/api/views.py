from rest_framework import status
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from app_utils.response import success_response, error_response
from .serializers import ConsultantRegisterSerializer


class ConsultantRegisterAPIView(APIView):
    # parser_classes = (MultiPartParser, FormParser)

    def post(self, request):
        serializer = ConsultantRegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.create_consultant(serializer.validated_data)
            return success_response(None, message="Your request has been received and is being processed")
        return error_response(serializer.errors)
