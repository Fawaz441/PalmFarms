from rest_auth.views import LoginView, LogoutView, APIView
from rest_auth.registration.views import RegisterView
from .serializers import UserSerializer, FarmSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from ..models import Farm
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK


class CustomRegisterView(RegisterView):
    def get_response(self):
        original_response = super().get_response()
        user = self.request.user
        user_data = UserSerializer(user).data
        original_response.data.update(user_data)
        return original_response


class CustomLogoutView(LogoutView):
    pass


class CustomLoginView(LoginView):
    def get_response(self):
        original_response = super().get_response()
        user = self.request.user
        user_data = UserSerializer(user).data
        original_response.data.update(user_data)
        return original_response


class FarmDetailView(APIView):
    permission_classes = (AllowAny, )

    def get(self, request):
        farm_id = request.GET.get('id')
        farm_obj = Farm.objects.get(id=int(farm_id))

        # Add views to the farm_obj
        farm_obj.views += 1
        farm_obj.save()

        data = FarmSerializer(farm_obj).data
        return Response({'data': data}, status=HTTP_200_OK)


class TopFarmersView(APIView):
    permission_classes = (AllowAny, )

    def get(self, request):
        # Would show top 3 results for farmers with most views and most sales

        max_results = 3
        most_viewed_farms = Farm.objects.all().order_by("-views")[:max_results]
        farms_with_most_sales = Farm.objects.all().order_by("-total_sales")[:max_results]

        most_viewed_farms_data = FarmSerializer(most_viewed_farms, many=True).data
        farms_with_most_sales_data = FarmSerializer(farms_with_most_sales, many=True).data

        data = {
            'most_viewed': most_viewed_farms_data,
            'most_sales': farms_with_most_sales_data
        }

        return Response({'data': data}, status=HTTP_200_OK)



