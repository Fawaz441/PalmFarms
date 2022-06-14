from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from phonenumber_field.modelfields import PhoneNumberField

DISPATCH_RIDER = 'DISPATCH RIDER'
PALM_RETAILER = 'RETAILER'
FARMER = 'FARMER'
INVESTOR = "INVESTOR"

USER_TYPES = [
    (DISPATCH_RIDER, DISPATCH_RIDER),
    (PALM_RETAILER, PALM_RETAILER),
    (FARMER, FARMER),
]


def get_surname_from_full_name(full_name):
    names = full_name.split()
    if len(names) > 1:
        return names[1]
    return names[0]


class UserManager(BaseUserManager):
    def create_superuser(self, phone_number, full_name, password):
        user = self.create_user(
            phone_number=phone_number,
            full_name=full_name,
        )
        user.is_superuser = True
        user.is_staff = True
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, phone_number, full_name, **fields):
        print(phone_number, full_name)
        user = User.objects.create(
            phone_number=phone_number,
            full_name=full_name,
            surname=get_surname_from_full_name(full_name),
            **fields
        )
        return user

# dispatch rider => full_name, phone_number, number_plate, location
# farmer => full_name, phone_number, farm_product
# palmRetailer => full_name, phone_number, farm_product


class User(AbstractBaseUser, PermissionsMixin):
    full_name = models.CharField(max_length=200)
    # since this will be used for login.
    surname = models.CharField(max_length=200)
    phone_number = PhoneNumberField(unique=True)
    number_plate = models.CharField(max_length=200, blank=True, null=True)
    location = models.CharField(max_length=500, blank=True, null=True)
    farm_product = models.CharField(max_length=500, blank=True, null=True)
    user_type = models.CharField(max_length=200, choices=USER_TYPES)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    objects = UserManager()

    USERNAME_FIELD = 'phone_number'
    EMAIL_FIELD = 'surname'
    REQUIRED_FIELDS = ['full_name']

    def get_short_name(self):
        return self.surname

    @property
    def first_name(self):
        return self.full_name.split()[0]

    @property
    def is_farmer(self):
        return self.user_type == FARMER

    @property
    def is_retailer(self):
        return self.user_type == PALM_RETAILER

    def __str__(self):
        return self.full_name


class Farm(models.Model):
    name = models.CharField(max_length=200)
    farmer = models.ForeignKey(
        User, related_name='farms', on_delete=models.CASCADE)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name

    @property
    def sample_products(self):
        return self.farm_products.all()[:5]


class FAQ(models.Model):
    question = models.TextField()
    answer = models.TextField()
    created = models.DateTimeField(auto_now=True)
    updated = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.question


class ContactMessage(models.Model):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    email = models.EmailField()
    phone_no = PhoneNumberField()
    message = models.TextField()

    def __str__(self):
        return self.first_name
