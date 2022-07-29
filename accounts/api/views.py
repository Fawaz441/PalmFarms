from rest_auth.views import LoginView, LogoutView, APIView
from rest_auth.registration.views import RegisterView
from .serializers import UserSerializer, FarmSerializer, NewsLetterMemberSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from ..models import Farm, NewsLetterMember, User, FarmView
from app_utils.response import success_response, error_response
from app_utils.time import get_midnight
from rest_framework.response import Response
from django.utils import timezone
from rest_framework.status import HTTP_200_OK
from accounts.permissions import IsFarmerPermission
from products.utils import get_farmer_farm
from products.models import Purchase, Product, ProductType
from .serializers import RegistrationSerializer, LoginSerializer


class CustomRegisterView(APIView):

    def post(self, request):
        data = RegistrationSerializer(data=request.data)
        if data.is_valid():
            data.save()
            return success_response()
        return error_response(data.errors)


class CustomLogoutView(LogoutView):
    pass


class CustomLoginView(APIView):
    def post(self, request):
        data = LoginSerializer(data=request.data)
        if data.is_valid():
            phone_number = data.validated_data.get("phone_number")
            password = data.validated_data.get("password")
            user = User.objects.filter(
                phone_number=phone_number).first()
            if not user:
                return error_response("Invalid credentials")
            if user.check_password(password):
                response_data = {"key": user.token}
                response_data.update(UserSerializer(user).data)
                return success_response(data=response_data)
            return error_response("Invalid credentials")
        return error_response(data.errors)


class FarmDetailView(APIView):
    permission_classes = (AllowAny, )

    def get(self, request):
        if request.GET.get('id') and not request.GET.get('type'):
            farm_id = request.GET.get('id')
            farm_obj = Farm.objects.get(id=int(farm_id))

            # Add views to the farm_obj
            farm_obj.views += 1
            farm_obj.save()

            data = FarmSerializer(farm_obj).data
            return Response({'data': data}, status=HTTP_200_OK)

        if not request.GET.get('id') and not request.GET.get('type'):
            all_farms = Farm.objects.all().order_by("name")
            data = FarmSerializer(
                all_farms, many=True).data
            return Response({'data': data}, status=HTTP_200_OK)

        if request.GET.get('type') and not request.GET.get('id'):
            type_ = request.GET.get('type')
            farm_type = ProductType.objects.filter(name__iexact=type_).first()
            if farm_type:
                farm_data = Farm.objects.filter(farm_products__type=farm_type)
                data = FarmSerializer(farm_data, many=True).data
                return Response({'data': data}, status=HTTP_200_OK)
            else:
                return Response({'data': []}, status=HTTP_200_OK)



class TopFarmersView(APIView):
    permission_classes = (AllowAny, )

    def get(self, request):
        # Would show top 3 results for farmers with most views and most sales

        max_results = 3
        most_viewed_farms = Farm.objects.all().order_by("-views")[:max_results]
        farms_with_most_sales = Farm.objects.all().order_by(
            "-total_sales")[:max_results]

        most_viewed_farms_data = FarmSerializer(
            most_viewed_farms, many=True).data
        farms_with_most_sales_data = FarmSerializer(
            farms_with_most_sales, many=True).data

        data = {
            'most_viewed': most_viewed_farms_data,
            'most_sales': farms_with_most_sales_data
        }

        return Response({'data': data}, status=HTTP_200_OK)


class NewsLetterSignUpAPIView(APIView):

    def post(self, request):
        data = NewsLetterMemberSerializer(data=request.data)
        if data.is_valid():
            email = data.validated_data.get("email")
            if NewsLetterMember.objects.filter(email=email).exists():
                return success_response(message="You are already a member of the PalmFarms newsletter")
            data.save()
            return success_response(message="Thank you for signing up to your newsletter!")
        return error_response(data.errors)


DAY = "day"
MONTH = "month"
YEAR = "year"


class DashboardAPIView(APIView):
    permission_classes = [IsFarmerPermission]

    def get(self, request):
        farm = get_farmer_farm(request.user)
        active_products = Product.objects.filter(
            farm=farm, is_active=True).count()
        return success_response(data={"active_products": active_products})


class NumberOfSalesAPIView(APIView):
    permission_classes = [IsFarmerPermission]

    def get(self, request):
        duration = request.GET.get("duration")
        if duration == DAY:
            sales = Purchase.objects.filter(
                farmer=request.user, time__gte=get_midnight()
            )
            return success_response(data={'sales': sales.count()})
        now = timezone.now()
        if duration == MONTH:
            sales = Purchase.objects.filter(
                time__month=now.month, time__year=now.year)
            return success_response(data={'sales': sales.count()})
        if duration == YEAR:
            sales = Purchase.objects.filter(time__year=now.year)
            return success_response(data={'sales': sales.count()})


class NumberOfFarmViewsAPIView(APIView):
    permission_classes = [IsFarmerPermission]

    def get(self, request):
        farm = get_farmer_farm(request.user)
        duration = request.GET.get("duration")
        if duration == DAY:
            views = FarmView.objects.filter(
                farm=farm, viewed_time=get_midnight()
            )
            return success_response(data={'views': views.count()})
        now = timezone.now()
        if duration == MONTH:
            views = FarmView.objects.filter(
                viewed_time__month=now.month, viewed_time__year=now.year)
            return success_response(data={'views': views.count()})
        if duration == YEAR:
            views = FarmView.objects.filter(viewed_time__year=now.year)
            return success_response(data={'views': views.count()})
