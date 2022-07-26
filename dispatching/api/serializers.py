from rest_framework import serializers
from dispatching.models import State, DispatchAddress


class StateSerializer(serializers.ModelSerializer):
    class Meta:
        model = State
        fields = ["id", "name", "capital"]


class UpdateDeliveryDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = DispatchAddress
        fields = ["state", "street_address"]
