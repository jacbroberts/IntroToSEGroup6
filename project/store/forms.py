from django import forms

class ProductAddForm(forms.Form):
    name = forms.CharField(label="Book Name", max_length=50,)
    price = forms.DecimalField(label="Price", max_value=100)
    remaining_quantity = forms.IntegerField(min_value=0)
    description = forms.CharField(required=False)
