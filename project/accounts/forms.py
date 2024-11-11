from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Customer, Seller
from django.contrib.auth import authenticate, login
class SellerEditForm(forms.Form):
    business_name = forms.CharField(label="Business Name", max_length=50)

class CustomerEditForm(forms.Form):
    street_address_1 = forms.CharField(label="Street Address", max_length=50)
    street_address_2 = forms.CharField(label="Street Address2 (optional)", max_length=50, required=False)
    city = forms.CharField(label="City",max_length=50)
    state = forms.CharField(label="State",max_length=2)
    zip_code = forms.CharField(label="Zip Code", max_length=5)

user_type_choices = [
    ('Customer','Customer'),
    ('Seller', 'Seller'),
    ('Admin', 'Admin'),
]

class CustomUserCreationForm(UserCreationForm):
    user_type = forms.ChoiceField(choices=user_type_choices)
    
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username","user_type","password1","password2")

class UserLoginForm(forms.Form):
    user_type = forms.ChoiceField(choices=user_type_choices)
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')

        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise forms.ValidationError('This user does not exist')
            if not user.check_password(password):
                raise forms.ValidationError('Incorrect username or password')
            if not user.is_active:
                raise forms.ValidationError('Account inactive')
        return cleaned_data 
    
    def login(self, request):
        if self.is_valid():
            username = self.cleaned_data.get('username')
            password = self.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return True
        return False
