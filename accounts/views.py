from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.views.generic import TemplateView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login, logout
from django.contrib import messages

from accounts.mixins import FarmerMixin, UnAuthenticatedUserMixin
from accounts.forms import DispatchRiderForm, PalmRetailerOrFarmerForm, UserLoginForm
from accounts.models import PALM_RETAILER, FARMER, DISPATCH_RIDER, INVESTOR, USER_TYPES, Farm, User, get_surname_from_full_name
from products.models import Product, Order

user_types = [PALM_RETAILER, FARMER, DISPATCH_RIDER, INVESTOR]


class PreSignupView(UnAuthenticatedUserMixin, View):
    def get(self, request):
        context = {'user_types': user_types}
        return render(request, 'auth/pre-signup.html', context)


class SignupView(UnAuthenticatedUserMixin, View):
    def get(self, request, type):
        if not type in user_types:
            return redirect('accounts:pre-signup')
        context = {}
        title = ""
        if type == PALM_RETAILER:
            form = PalmRetailerOrFarmerForm
            title = "Be A PalmRetailer"
        elif type == FARMER:
            form = PalmRetailerOrFarmerForm
            title = "Be A PalmFarmer"
        elif type == DISPATCH_RIDER:
            form = DispatchRiderForm
            title = "Join Our Dispatch Team"
        context = {'form': form, 'title': title, 'type': type}
        return render(request, 'auth/signup.html', context)

    def post(self, request, type):
        if type == FARMER or type == PALM_RETAILER:
            form = PalmRetailerOrFarmerForm(data=request.POST)
        if type == DISPATCH_RIDER:
            form = DispatchRiderForm(data=request.POST)
        if form.is_valid():
            phone_number = form.cleaned_data.get('phone_number')
            if User.objects.filter(phone_number=phone_number).exists():
                messages.error(
                    request, "An account with this phone number already exists")
                return redirect(request.META.get('HTTP_REFERER'))
            new_user = form.save(commit=False)
            new_user.user_type = type
            new_user.surname = get_surname_from_full_name(new_user.full_name)
            new_user.save()
            if(type == FARMER):
                Farm.objects.create(
                    name=f'{new_user.full_name} Farmers',
                    farmer=new_user
                )
            messages.success(request, "Sign up successful")
            return redirect("accounts:login")
        else:
            messages.error(request, form.errors.as_text())
            return redirect(request.META.get('HTTP_REFERER'))


class LoginView(UnAuthenticatedUserMixin, View):
    def get(self, request):
        form = UserLoginForm()
        return render(request, "auth/login.html", context={'form': form})

    def post(self, request):
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            surname = form.cleaned_data.get("surname")
            phone_number = form.cleaned_data.get("phone_number")
            user = User.objects.filter(
                full_name__icontains=surname, phone_number=phone_number).first()
            if user:
                messages.success(request, 'Login successful')
                login(request, user)
                return redirect('accounts:user-view')
            else:
                messages.error(request, 'Invalid credentials')
                return redirect(request.META.get('HTTP_REFERER'))
        else:
            messages.error(request, form.errors.as_text())
            return redirect(request.META.get('HTTP_REFERER'))


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect("accounts:login")


class DashboardView(FarmerMixin, View):
    def get(self, request):
        total_products = Product.objects.filter(
            available_stock__gt=0, farm__farmer=request.user).count()
        orders = Order.objects.filter(
            customer__isnull=False, items__product__farm__farmer=request.user)
        total_customers = orders.values('customer_id').count()
        online_orders = orders.filter(delivered=False).count()
        context = {'total_products': total_products,
                   'total_customers': total_customers,
                   'online_orders': online_orders
                   }
        return render(request, 'pages/dashboard.html', context)


class UserSpecificView(LoginRequiredMixin, View):
    def get(self, request):
        if not request.user.is_authenticated:
            return redirect("accounts:login")
        if request.user.is_farmer:
            return redirect("accounts:dashboard")
        else:
            return redirect("products:farms")
