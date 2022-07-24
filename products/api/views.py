import random
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from app_utils.response import success_response, error_response
from products.models import Product, Cart, CartProduct, ProductType, Coupon
from .pagination import ProductsPagination
from .serializers import (ProductSerializer, ProductDetailSerializer,
                          CartSerializer, ProductTypeSerializer, AddToCartSerializer, CouponSerializer,
                          DeliveryDetailsSerializer)


class ProductTypesAPIView(APIView):
    def get(self, request):
        product_types = ProductType.objects.all()
        return success_response(data=ProductTypeSerializer(product_types, many=True).data)


class ProductsListAPIView(ListAPIView):
    pagination_class = ProductsPagination

    def get(self, request, *args, **kwargs):
        filters = {}
        product_type = request.GET.get("product_type")
        if product_type and product_type != 'all':
            filters['type__name'] = product_type
        queryset = Product.objects.filter(
            is_active=True, available_stock__gt=0, **filters)
        serializer = ProductSerializer(queryset, many=True)
        page = self.paginate_queryset(serializer.data)
        return success_response(data=self.get_paginated_response(page))


class FeaturedProductsAPIView(APIView):
    def get(self, request):
        products = Product.objects.filter(
            is_active=True, available_stock__gt=0)[:8]
        serializer = ProductSerializer(products, many=True)
        return success_response(data=serializer.data)


class ProductDetailAPIView(APIView):
    def get(self, request):
        tag = request.GET.get("tag")
        if tag:
            product = Product.objects.filter(tag=tag).first()
            if not product:
                return error_response("Product not found")
            random_products = list(Product.objects.exclude(
                tag=tag).filter(type=product.type))
            random_products = random.sample(random_products, 4)
            data = {'data': ProductDetailSerializer(
                product).data, 'similar_products': ProductSerializer(random_products, many=True).data}
            return success_response(data)
        return error_response("Product not found")


class AddToCartAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, product_id):
        data = AddToCartSerializer(data=request.data)
        if data.is_valid():
            quantity = data.validated_data.get("quantity")
            product = Product.objects.filter(id=product_id).first()
            if not product:
                return error_response("Product does not exist.")
            if product.available_stock == 0:
                return error_response("Product out of stock")
            user_cart, _ = Cart.objects.get_or_create(
                user=request.user, ordered=False)
            if _:
                cart_product = CartProduct.objects.create(
                    product=product,
                    quantity=quantity
                )
                user_cart.items.add(cart_product)
                cart = CartSerializer(user_cart).data
                return success_response(message="Product added successfully", data=cart)
            cart_product = user_cart.items.filter(
                product__id=product_id).first()
            if cart_product:
                cart_product.quantity = quantity
                cart_product.save()
                cart = CartSerializer(user_cart).data
                return success_response(message="Product added successfully", data=cart)
            cart_product = CartProduct.objects.create(
                product=product, quantity=quantity)
            user_cart.items.add(cart_product)
            user_cart.save()
            cart = CartSerializer(user_cart).data
            return success_response(message="Product added successfully", data=cart)
        return error_response(data.errors)


class RemoveFromCartAPIView(APIView):
    def post(self, request, cart_product_id):
        user_cart, _ = Cart.objects.get_or_create(
            user=request.user, ordered=False)
        cart_product = CartProduct.objects.filter(id=cart_product_id).first()
        user_cart.items.remove(cart_product)
        user_cart.save()
        cart = CartSerializer(user_cart).data
        return success_response(message="Product removed successfully", data=cart)


class CartAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        user_cart, _ = Cart.objects.get_or_create(
            user=request.user, ordered=False)
        return success_response(data=CartSerializer(user_cart).data)


class AddCouponAPIView(APIView):
    def post(self, request):
        data = CouponSerializer(data=request.data)
        if data.is_valid():
            code = data.validated_data.get("code")
            user_cart = Cart.objects.filter(
                ordered=False, user=request.user).first()
            if not user_cart:
                return error_response("You don't have any items in your cart")
            if user_cart.items.count() == 0:
                return error_response("You don't have any items in your cart")
            coupon = Coupon.objects.filter(code=code).first()
            if coupon:
                if user_cart.coupon == coupon:
                    return error_response("This coupon is already applied to your cart")
                other_uses = Cart.objects.filter(coupon=coupon).count()
                if other_uses == coupon.max_use or coupon.expired or (coupon.expiry_date and (coupon.expiry_date > timezone.now())):
                    return error_response("This coupon has expired")
                user_cart.coupon = coupon
                user_cart.save()
                return success_response(data=CartSerializer(user_cart).data, message="Coupon added successfully")
            return error_response("Invalid coupon.")
        return error_response(data.errors)


class DeliveryDetailsAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user_cart, _ = Cart.objects.get_or_create(
            ordered=False, user=request.user)
        data = DeliveryDetailsSerializer(user_cart).data
        return success_response(data=data)
