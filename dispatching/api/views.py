from rest_framework.views import APIView
from dispatching.models import State
from app_utils.response import success_response
from .serializers import StateSerializer


class StateListAPIView(APIView):
    def get(self, request):
        states = State.objects.all()
        data = StateSerializer(states, many=True).data
        return success_response(data)
