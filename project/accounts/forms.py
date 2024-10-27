from django import forms

class SellerEditForm(forms.Form):
    business_name = forms.CharField(label="Business Name", max_length=50)

class CustomerEditForm(forms.Form):
    street_address_1 = forms.CharField(label="Street Address", max_length=50)
    street_address_2 = forms.CharField(label="Street Address2 (optional)", max_length=50, required=False)
    city = forms.CharField(label="City",max_length=50)
    state = forms.CharField(label="State",max_length=2)
    zip_code = forms.CharField(label="Zip Code", max_length=5)