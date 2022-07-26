from rest_framework import serializers
from ..models import User, FARMER, Farm
from django.db.utils import IntegrityError
from ..utils import send_welcome_sms


# Anyone of the user types (dispatchers, farmers or retailers will login with phone number and a unique password)
class SignInSerializer(serializers.Serializer):
    phone_number = serializers.CharField()
    password = serializers.CharField()
    user = None

    def throw_error(self):
        raise serializers.ValidationError(
            "Unable to login with provided credentials.")

    def validate(self, data):
        password = data.get('password')
        user = User.objects.filter(
            phone_number__iexact=data['phone_number']).first()

        if user:
            if user.check_password(password):
                data['user'] = user
                return data
            else:
                self.throw_error()
        else:
            self.throw_error()


class RegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(
        style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = User
        fields = ['phone_number', 'first_name', 'last_name',
                  'password', 'password2', 'user_type']
        extra_kwargs = {
            'password': {
                'write_only': True
            }
        }

    def save(self, request):
        user = User(
            phone_number=self.validated_data['phone_number'],
            first_name=self.validated_data['first_name'],
            last_name=self.validated_data['last_name'],
            user_type=self.validated_data['user_type'],
        )

        password = self.validated_data['password']
        password2 = self.validated_data['password2']

        if password != password2:
            raise serializers.ValidationError(
                {'error': 'Passwords must match.'})
        user.set_password(password)
        try:
            user.save()
            if self.validated_data.get('user_type') == FARMER:
                Farm.objects.create(
                    name=f'{user.first_name} {user.last_name} Farmers',
                    farmer=user
                )
            send_welcome_sms(user, password)
            return user
        except IntegrityError:
            raise serializers.ValidationError(
                {'error': 'User with this phone number already exists.'})


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'phone_number',
                  'profile_pic', 'user_type',)
