import calendar
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.template.loader import get_template
from django.utils import timezone
from django.utils.dates import MONTHS
from products.models import Cart, Product, Payment


@login_required
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


@login_required
def get_payments(request):
    month = request.GET.get('month')
    year = request.GET.get('year')
    query_params = {'timestamp__year': year, 'timestamp__month': month}
    if(request.user.is_farmer):
        query_params['farmer'] = request.user
    else:
        query_params['customer'] = request.user
    payments = Payment.objects.filter(**query_params).order_by('-timestamp')
    data = get_template(
        'pages/payments/payment-list-rows.html').render({'payments': payments})
    return JsonResponse(data={'data': data})


@login_required
def get_sales(request):
    time_type = request.GET.get('type')
    now = timezone.now()
    data = {}
    if time_type == 'year':
        years = [year for year in range(now.year, now.year - 5, -1)]
        for year in years:
            data[year] = Cart.objects.filter(
                ordered=True, delivered=True, farmer=request.user, ordered_date__year=year).count()
    if time_type == 'month':
        current_month = now.month
        for month in MONTHS:
            if month <= current_month:
                data[str(MONTHS[month])] = Cart.objects.filter(
                    ordered=True, delivered=True,
                    farmer=request.user, ordered_date__year=now.year,
                    ordered_date__month=month).count()
    if time_type == 'week':
        month = int(request.GET.get('month', 1))
        days = calendar.monthrange(now.year, int(month))
        end = days[1]
        if month == now.month:
            end = now.day+1
        for day in range(1, end):
            stringed_timestamp = f"{now.day}.{now.month}.{now.year}T0:0:0"
            data[stringed_timestamp] = Cart.objects.filter(
                ordered=True, delivered=True, farmer=request.user,
                ordered_date__year=now.year,
                ordered_date__month=month,
                ordered_date__day=day
            ).count()
    return JsonResponse({'data': data})


def get_payment_reference(request):
    order_id = request.GET.get('order')
    now = timezone.now()
    order = Cart.objects.filter(
        ordered=False,
        delivered=False,
        user=request.user,
        id=order_id
    ).first()
    if order:
        new_ref = f"ORDER--{order_id}--{request.user.id}"
        order.reference = new_ref
        order.save()
        return JsonResponse({'data': new_ref})
    else:
        return JsonResponse({'error': 'Error.'}, status=400)


def update_order(request):
    order_id = request.GET.get('order')
    order = Cart.objects.filter(
        ordered=False,
        delivered=False,
        user=request.user,
        id=order_id
    ).first()
    order.ordered = True
    order.ordered_date = timezone.now()
    order.save()
    return JsonResponse({'message': 'Success'})
