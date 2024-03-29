from django.forms import Form, ModelForm, CharField
from phonenumber_field.formfields import PhoneNumberField

from accounts.models import User, ContactMessage


class UserLoginForm(Form):
    surname = CharField(max_length=200, label="Surname")
    phone_number = PhoneNumberField(label="Phone No")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': 'bg-white border border-primary rounded-[10px] h-[82px] p-[10px] text-[25px]'
            })

        self.fields['surname'].widget.attrs.update({'autofocus': 'on'})


class PalmRetailerOrFarmerForm(ModelForm):
    class Meta:
        model = User
        fields = ['full_name', 'phone_number', 'farm_product']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': 'bg-white border border-primary rounded-[10px] h-[82px] p-[10px] text-[25px]'
            })
            self.fields[field].required = True


class DispatchRiderForm(ModelForm):
    class Meta:
        model = User
        fields = ['full_name', 'phone_number', 'number_plate', 'location']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': 'bg-white border border-primary rounded-[10px] h-[82px] p-[10px] text-[25px]'
            })
            self.fields[field].required = True


class ContactMessageForm(ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['message', 'first_name',
                  'last_name',
                  'email',
                  'phone_no']
