from accounts.mixins import FarmerMixin
from accounts.models import Farm
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.views.generic import View, ListView

from .forms import ProductForm
from .models import Product, ProductType


class AddProductView(FarmerMixin, View):
    def get(self, request):
        form = ProductForm()
        context = {'form': form}
        return render(request, 'pages/products/add-product.html', context)

    def post(self, request):
        form = ProductForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            data = form.save(commit=False)
            data.owner = request.user
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
            products = Product.objects.order_by('farm__name')
        if category:
            products = products.filter(type=category)
        return products

    def get_template_names(self):
        if not self.request.user.is_farmer:
            return ["pages/products/farm-list.html"]
        else:
            return ["pages/products/product-list.html"]
