from rest_framework.serializers import (
    Serializer, ModelSerializer, IntegerField, CharField, DateTimeField)
from dispatching.api.serializers import UpdateDeliveryDetailsSerializer
from products.models import (
    Product, ProductType, ProductVariation, Cart, CartProduct, Coupon)


class AddToCartSerializer(Serializer):
    quantity = IntegerField()


class VariationSerializer(ModelSerializer):
    class Meta:
        model = ProductVariation
        fields = ["id", "name"]


class ProductSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = ["name", "selling_price",
                  "product_image", "type", "discount", "id", "tag", "description"]


class ProductTypeSerializer(ModelSerializer):
    class Meta:
        model = ProductType
        fields = ["name", "id"]


class ProductDetailSerializer(ModelSerializer):
    variations = VariationSerializer(many=True)

    class Meta:
        model = Product
        fields = ["name", "selling_price",
                  "product_image", "type", "discount", "id", "tag", "description", "variations"]


class CartProductSerializer(ModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = CartProduct
        fields = ["product", "quantity", "id", "total_cost"]


class AddCouponSerializer(Serializer):
    code = CharField()


class CouponSerializer(ModelSerializer):
    class Meta:
        model = Coupon
        fields = ["code", "value", "is_amount"]


class CartSerializer(ModelSerializer):
    items = CartProductSerializer(many=True)
    coupon = CouponSerializer()

    class Meta:
        model = Cart
        fields = ["delivery_address", "items",
                  "total_cost", "delivery_fee", "subtotal", "discount", "coupon", "id"]


class DeliveryDetailsSerializer(ModelSerializer):
    first_name = CharField(source='user.first_name')
    last_name = CharField(source="user.last_name")
    phone = CharField(source="user.phone_number")
    delivery_address = UpdateDeliveryDetailsSerializer()

    class Meta:
        model = Cart
        fields = ["first_name", "last_name", "phone", "delivery_address"]


class AddProductSerializer(ModelSerializer):
    start_date = DateTimeField(required=False)

    class Meta:
        model = Product
        fields = ['name', 'cost_price', 'selling_price',
                  'description', 'available_stock', 'type', 'image', 'start_date']
