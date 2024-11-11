# store/forms.py
from django import forms

class PaymentForm(forms.Form):
    card_number = forms.CharField(max_length=16, min_length=16, required=True)
    expiry_date = forms.RegexField(regex=r'(0[1-9]|1[0-2])\/?([0-9]{2})', required=True)
    cvv = forms.CharField(max_length=3, min_length=3, required=True)
    billing_address = forms.CharField(required=True)
    billing_city = forms.CharField(required=True)
    billing_state = forms.CharField(required=True)
    billing_zip = forms.RegexField(regex=r'^\d{5}$', required=True)
    different_shipping = forms.BooleanField(required=False)
    shipping_address = forms.CharField(required=False)
    shipping_city = forms.CharField(required=False)
    shipping_state = forms.CharField(required=False)
    shipping_zip = forms.RegexField(regex=r'^\d{5}$', required=False)


class ProductAddForm(forms.Form):
    name = forms.CharField(label="Book Name", max_length=50,)
    price = forms.DecimalField(label="Price", max_value=100)
    remaining_quantity = forms.IntegerField(min_value=0)
    description = forms.CharField(required=False)

