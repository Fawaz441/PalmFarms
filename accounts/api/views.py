from rest_auth.views import LoginView, LogoutView, APIView
from rest_auth.registration.views import RegisterView
from .serializers import UserSerializer, FarmSerializer, NewsLetterMemberSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from ..models import Farm, NewsLetterMember, User
from app_utils.response import success_response, error_response
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
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
