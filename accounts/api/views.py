from django.db.models import Sum
from rest_auth.views import LoginView, LogoutView, APIView
from rest_auth.registration.views import RegisterView
from .serializers import UserSerializer, FarmSerializer, NewsLetterMemberSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from ..models import Farm, NewsLetterMember, User, FarmView
from app_utils.response import success_response, error_response
from app_utils.time import get_midnight, date_hour, date_month
from rest_framework.response import Response
from django.utils import timezone
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND
from accounts.permissions import IsFarmerPermission
from products.utils import get_farmer_farm
from products.models import Purchase, Product, ProductType
from .serializers import RegistrationSerializer, LoginSerializer
from .pagination import FarmsPagination
from app_utils.response import success_response, error_response
from rest_framework.generics import ListAPIView


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
        if request.GET.get('id'):
            farm_id = request.GET.get('id')
            farm_obj = Farm.objects.get(id=int(farm_id))

            if farm_obj:
                # Add views to the farm_obj
                farm_obj.views += 1
                farm_obj.save()

                serializer = FarmSerializer(
                    farm_obj)
                data = serializer.data
                return Response({"data": data}, status=HTTP_200_OK)
            else:
                return Response({"data": []}, status=HTTP_404_NOT_FOUND)
        else:
            return Response({"error": "You need to pass a farm ID"}, status=HTTP_400_BAD_REQUEST)


class FarmListView(ListAPIView):
    permission_classes = (AllowAny, )
    pagination_class = FarmsPagination

    def get(self, request):
        if not request.GET.get('type'):
            all_farms = Farm.objects.all().order_by("name")
            serializer = FarmSerializer(
                all_farms, many=True)
            page = self.paginate_queryset(serializer.data)
            return success_response(data=self.get_paginated_response(page))

        if request.GET.get('type'):
            type_ = request.GET.get('type')
            print("type", type_)
            farm_type = ProductType.objects.filter(name__iexact=type_).first()
            if farm_type and type_.lower() != "all":
                farm_data = Farm.objects.filter(farm_products__type=farm_type)
                serializer = FarmSerializer(
                    farm_data, many=True)
                page = self.paginate_queryset(serializer.data)
                return success_response(data=self.get_paginated_response(page))
            elif type_.lower() == "all":
                all_farms = Farm.objects.all().order_by("name")
                serializer = FarmSerializer(
                    all_farms, many=True)
                page = self.paginate_queryset(serializer.data)
                return success_response(data=self.get_paginated_response(page))
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
                farmer=request.user,
                time__month=now.month, time__year=now.year)
            return success_response(data={'sales': sales.count()})
        if duration == YEAR:
            sales = Purchase.objects.filter(
                farmer=request.user, time__year=now.year)
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
                viewed_time__month=now.month, viewed_time__year=now.year, farm=farm)
            return success_response(data={'views': views.count()})
        if duration == YEAR:
            views = FarmView.objects.filter(
                viewed_time__year=now.year, farm=farm)
            return success_response(data={'views': views.count()})


class SalesAggregateAPIView(APIView):
    permission_classes = [IsFarmerPermission]

    def get(self, request):
        farm = get_farmer_farm(request.user)
        duration = request.GET.get("duration")
        data = {}
        now = timezone.now()
        if duration == DAY:
            midnight = get_midnight()
            for hour in range(midnight.hour, now.hour+1):
                timestamp = timezone.datetime(
                    now.year, now.month, now.day, hour, 0, 0)
                sales = Purchase.objects.filter(
                    farmer=request.user,
                    time__day=now.day, time__month=now.month, time__year=now.year, time__hour=hour) \
                    .aggregate(total=Sum('amount')).get('total') or 0
                data[date_hour(timestamp)] = sales
            return success_response(data=data)
        if duration == MONTH:
            year = now.year
            for month in range(1, now.month + 1):
                timestamp = timezone.datetime(now.year, month, 1)
                sales = Purchase.objects.filter(
                    farmer=request.user,
                    time__month=month, time__year=now.year,) \
                    .aggregate(total=Sum('amount')).get('total') or 0
                data[date_month(timestamp)] = sales
            return success_response(data=data)
        if duration == YEAR:
            for year in range(2022, now.year+1):
                sales = Purchase.objects.filter(
                    farmer=request.user,
                    time__year=year) \
                    .aggregate(total=Sum('amount')).get('total') or 0
                data[year] = sales
            return success_response(data=data)
        return error_response("Invalid year")


class FinancialScoreAPIView(APIView):
    permission_classes = [IsFarmerPermission]

    def get(self, request):
        target = 10000
        started_date = request.user.date_joined
        total_sales = 0
        total_target = 0
        now = timezone.now()

        for year in range(started_date.year, now.year+1):
            if year == started_date.year:
                first_month = started_date.month
            else:
                first_month = 1
            for month in range(first_month, 13):
                total_target += target
                total_sales += Purchase.objects.filter(time__month=month, time__year=year).aggregate(
                    total=Sum('amount')).get("total") or 0
        fin_score = (total_sales/total_target) * 100
        midnight = get_midnight()
        sales_in_current_month = Purchase.objects.filter(time__month=now.month, time__year=now.year).aggregate(
            total=Sum('amount')).get("total") or 0
        sales_in_current_year = Purchase.objects.filter(time__year=now.year).aggregate(
            total=Sum('amount')).get("total") or 0
        return success_response(data={
            'fin_score': fin_score,
            'sales_in_current_month': sales_in_current_month,
            "sales_in_current_year": sales_in_current_year,
            "eligible_for_loan": fin_score > 75
        })
