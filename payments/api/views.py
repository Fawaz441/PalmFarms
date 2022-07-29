from accounts.permissions import IsFarmerPermission
from app_utils.response import success_response, error_response
from app_utils.constants import SETTLED
from payments.models import FarmerSettlement
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from .pagination import PaymentsPagination
from .serializers import PaymentSerializer


class PaymentsListAPIView(ListAPIView):
    permission_classes = [IsFarmerPermission]
    pagination_class = PaymentsPagination

    def get(self, request, *argws, **kwargs):
        payments = FarmerSettlement.objects.filter(
            purchase__farmer=request.user)
        serializer = PaymentSerializer(payments, many=True)
        page = self.paginate_queryset(serializer.data)
        return success_response(data=self.get_paginated_response(page))
