from django.urls import path
from .views import (ProductsListAPIView, FeaturedProductsAPIView,
                    ProductDetailAPIView, AddToCartAPIView, ProductTypesAPIView,
                    CartAPIView, RemoveFromCartAPIView, AddCouponAPIView, DeliveryDetailsAPIView,
                    FarmerProductsAPIView, UpdateDeliveryDetails, OrderCartAPIView, PayStackWebhookAPIView,
                    AddProductAPIView)

urlpatterns = [
    path('', ProductsListAPIView.as_view()),
    path('featured-products', FeaturedProductsAPIView.as_view()),
    path('detail', ProductDetailAPIView.as_view()),
    path('add-to-cart/<int:product_id>', AddToCartAPIView.as_view()),
    path('remove-from-cart/<int:cart_product_id>',
         RemoveFromCartAPIView.as_view()),
    path('product-types', ProductTypesAPIView.as_view()),
    path('cart', CartAPIView.as_view()),
    path('add-coupon', AddCouponAPIView.as_view()),
    path('delivery-details', DeliveryDetailsAPIView.as_view()),
    path('farmer-products', FarmerProductsAPIView.as_view()),
    path('update-delivery-address/<int:cart_id>',
         UpdateDeliveryDetails.as_view()),
    path('order-cart/<int:cart_id>', OrderCartAPIView.as_view()),
    path('paystack/dahdoefyr3eu9hcdsigrsdlf',
         PayStackWebhookAPIView.as_view()),
    path('add-product', AddProductAPIView.as_view())
]
