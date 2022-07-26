from rest_auth.views import LoginView, LogoutView, APIView
from rest_auth.registration.views import RegisterView
from .serializers import UserSerializer


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
