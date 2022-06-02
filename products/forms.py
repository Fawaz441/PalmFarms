from django import forms
from .models import Product


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'cost_price',
                  'selling_price', 'available_stock', 'image', 'type']
        labels = {
            'name': "Name of the Product",
            "available_stock": "Items available",
            "image": "Upload a picture"
        }

    def __init__(self, *args, **kwargs):
        styled_fields = ['name', 'cost_price',
                         'selling_price', 'available_stock', 'type']
        super().__init__(*args, **kwargs)
        for field in styled_fields:
            self.fields[field].widget.attrs.update({
                'class': 'bg-[#94E56D]/[0.69] rounded-lg h-[58px] w-full p-3 text-3xl mb-2'
            })


class BankPaymentConfirmationForm(forms.Form):
    amount = forms.DecimalField()
    order = forms.IntegerField()
