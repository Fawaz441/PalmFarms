from django.http import JsonResponse
from products.models import Product


def adjust_product_quantity(request):
    product = request.POST.get('product')
    action = request.POST.get('action')

    if not product:
        return JsonResponse(data={'error': 'No product specified'}, status=400)
    product = Product.objects.filter(
        id=product, farm__farmer=request.user).first()
    if not product:
        return JsonResponse(data={'error': 'No product found'}, status=400)
    product.available_stock = product.available_stock + \
        1 if action == 'plus' else product.available_stock - 1
    product.save()
    return JsonResponse(data={'new_quantity': product.available_stock, 'message': 'Quantity adjusted successfully'})
