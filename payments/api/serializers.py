from rest_framework import serializers
from payments.models import FarmerSettlement
from products.api.serializers import PurchaseSerializer


class PaymentSerializer(serializers.ModelSerializer):
    purchase = PurchaseSerializer()

    class Meta:
        model = FarmerSettlement
        fields = [
            "status",
            "updated",
            "success_timestamp",
            "purchase"
        ]
