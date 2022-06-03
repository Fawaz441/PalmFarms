from .models import Payment, Product, ProductType, Cart, CartProduct
from .forms import BankPaymentConfirmationForm, ProductForm
from products.utils import confirm_bank_payment
from django.utils.dates import MONTHS
from products.utils import confirm_bank_payment, get_months_options
from django.utils.timezone import now
from email import message
from accounts.mixins import FarmerMixin
from accounts.models import Farm
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.views.generic import View, ListView


def get_years():
    today = now()
    years = []
    for year in range(today.year, today.year-5, -1):
        years.append(year)
    return years


class AddProductView(FarmerMixin, View):
    def get(self, request):
        form = ProductForm()
        context = {'form': form}
        return render(request, 'pages/products/add-product.html', context)

    def post(self, request):
        form = ProductForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            data = form.save(commit=False)
            data.farm = Farm.objects.filter(farmer=request.user).first()
            print(data.farm, data)
            data.save()
            messages.success(request, "Product created successfully")
            return redirect(request.META.get("HTTP_REFERER"))
        else:
            messages.error(request, form.errors.as_text())
            return redirect(request.META.get("HTTP_REFERER"))


class ProductListView(LoginRequiredMixin, ListView):
    model = Product
    context_object_name = 'products'
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        producttypes = ProductType.objects.all()
        context['producttypes'] = producttypes
        return context

    def get_queryset(self):
        user = self.request.user
        category = self.request.GET.get('category')
        if user.is_farmer:
            products = Product.objects.filter(
                farm__farmer=user).order_by('farm__name')
        else:
            products = Product.objects.filter(
                available_stock__gt=0).order_by('farm__name')
        if category:
            products = products.filter(type=category)
        return products

    def get_template_names(self):
        if not self.request.user.is_farmer:
            return ["pages/products/farm-list.html"]
        else:
            return ["pages/products/product-list.html"]


class PaymentListView(LoginRequiredMixin, ListView):
    model = Payment
    template_name = "pages/payments/payment-list.html"
    context_object_name = "payments"

    def get_current_time(self):
        today = now()
        return {'month': today.month, 'year': today.year}

    def get_queryset(self):
        user = self.request.user
        time = self.get_current_time()
        if user.is_farmer:
            return Payment.objects.filter(farmer=user, timestamp__year=time['year'], timestamp__month=time['month'])
        return Payment.objects.filter(customer=user, timestamp__year=time['year'], timestamp__month=time['month'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        months = get_months_options()
        now = self.get_current_time()
        context['months'] = months
        context['years'] = get_years()
        context['current_month'] = now['month']
        context['current_year'] = now['year']
        return context


class AddToCart(LoginRequiredMixin, View):

    def redirect_user(self, request, message=None):
        if message:
            messages.success(request, message)
        return redirect(request.META.get('HTTP_REFERER'))

    def get(self, request, product_id):
        product = Product.objects.filter(id=product_id).first()
        if not product:
            return self.redirect_user(request, "Product does not exist.")
        if product.available_stock == 0:
            return self.redirect_user(request, "Product out of stock")
        user_cart, _ = Cart.objects.get_or_create(
            user=request.user, delivered=False, ordered=False)
        if _:
            cart_product = CartProduct.objects.create(
                product=product
            )
            user_cart.items.add(cart_product)
            return self.redirect_user(request, "Product added successfully")
        cart_product = user_cart.items.filter(product__id=product_id).first()
        if cart_product:
            cart_product.quantity += 1
            cart_product.save()
            return self.redirect_user(request, "Product added successfully")
        cart_product = CartProduct.objects.create(product=product)
        user_cart.items.add(cart_product)
        user_cart.save()
        return self.redirect_user(request, "Product added successfully")


class CheckoutView(LoginRequiredMixin, View):
    def get(self, request):
        user_cart = Cart.objects.filter(
            user=request.user, delivered=False, ordered=False).prefetch_related('items').first()
        context = {'cart': user_cart}
        return render(request, 'pages/products/cart.html', context)


class ConfirmBankPayment(LoginRequiredMixin, View):
    def post(self, request):
        data = BankPaymentConfirmationForm(data=request.POST)
        if data.is_valid():
            order = data.cleaned_data.get('order')
            amount = data.cleaned_data.get('amount')
            order = Cart.objects.get(id=order)
            if not order:
                messages.error(request, "Cart not found")
                return redirect(request.META.get("HTTP_REFERER"))
            confirm_bank_payment(order, amount)
            messages.success(
                request, "Successful!. Please wait while we confirm your order")
            return redirect("accounts:user-view")
        else:
            messages.error(request, "invalid")
            return redirect(request.META.get("HTTP_REFERER"))
