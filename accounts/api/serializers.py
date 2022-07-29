from rest_framework import serializers
from ..models import User, FARMER, Farm, NewsLetterMember
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


class RegistrationSerializer(serializers.Serializer):
    password2 = serializers.CharField(
        style={'input_type': 'password'}, write_only=True)
    password = serializers.CharField(
        style={'input_type': 'password'}, write_only=True)
    phone_number = serializers.CharField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    user_type = serializers.CharField()
    # class Meta:
    #     model = User
    #     fields = ['phone_number', 'first_name', 'last_name',
    #               'password', 'password2', 'user_type']
    #     extra_kwargs = {
    #         'password': {
    #             'write_only': True
    #         }
    #     }

    def validate_phone_number(self, phone_number):
        print(phone_number, 'phone no')
        if len(phone_number) == 11 and phone_number.startswith("0"):
            return "+234" + phone_number[1:]
        if phone_number.startswith("+234") and len(phone_number) == 14:
            return phone_number
        raise serializers.ValidationError("Invalid phone number")

    def save(self):
        full_name = first_name = self.validated_data.get(
            'first_name', " ") + " " + self.validated_data.get('last_name', " "),
        user = User(
            phone_number=self.validated_data['phone_number'],
            first_name=self.validated_data['first_name'],
            last_name=self.validated_data['last_name'],
            user_type=self.validated_data['user_type'],
            full_name=full_name

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
                    name=f"{user.first_name} {user.last_name}'s Farm",
                    farmer=user
                )
            send_welcome_sms(user, password)
            return user
        except IntegrityError:
            raise serializers.ValidationError(
                {'error': 'User with this phone number already exists.'})


class LoginSerializer(serializers.Serializer):
    phone_number = serializers.CharField()
    password = serializers.CharField()

    def validate_phone_number(self, phone_number):
        if len(phone_number) == 11 and phone_number.startswith("0"):
            return "+234" + phone_number[1:]
        if phone_number.startswith("+234") and len(phone_number) == 14:
            return phone_number
        raise serializers.ValidationError("Invalid phone number")


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'phone_number',
                  'profile_pic', 'user_type',)


class FarmSerializer(serializers.ModelSerializer):
    farmer = UserSerializer()

    class Meta:
        model = Farm
        fields = ('id', 'name', 'farmer', 'views', 'total_sales')


class NewsLetterMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsLetterMember
        fields = ["email"]
