from django.shortcuts import render
from django.http import HttpResponse
from .forms import SellerEditForm, CustomerEditForm

# Create your views here.

from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic import CreateView
from .models import Seller, Customer
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required, permission_required

class SignUpView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"

@login_required
def make_seller(request):
    if Seller.objects.filter(user = request.user).exists():
        return HttpResponseRedirect(reverse('accounts:seller_edit'))
    else:
        s = Seller.objects.create(user=request.user, business_name="")
        return HttpResponseRedirect(reverse('accounts:seller_edit'))


@login_required
def make_customer(request):
    if Customer.objects.filter(user=request.user).exists():
        return HttpResponseRedirect(reverse('accounts:customer_edit'))
    else:
        c = Customer.objects.create(user=request.user, street_address_1="", street_address_2="", city="", state="", zip_code="")
        return HttpResponseRedirect(reverse('accounts:customer_edit'))
    



@login_required
def edit_seller(request):
    seller_instance = get_object_or_404(Seller, user=request.user)

    # If this is a POST request then process the Form data
    if request.method == 'POST':

        # Create a form instance and populate it with data from the request (binding):
        form = SellerEditForm(request.POST)

        # Check if the form is valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)
            seller_instance.business_name = form.cleaned_data['business_name']
            seller_instance.save()

            # redirect to a new URL:
            return HttpResponseRedirect(reverse('home'))

    # If this is a GET (or any other method) create the default form.
    else:
        form = SellerEditForm(initial={'business_name': ""})

    context = {
        'form': form,
        'seller_instance': seller_instance,
    }

    return render(request, 'registration/edit_seller.html', context)

@login_required
def edit_customer(request):
    customer_instance = get_object_or_404(Customer, user=request.user)

    # If this is a POST request then process the Form data
    if request.method == 'POST':

        # Create a form instance and populate it with data from the request (binding):
        form = CustomerEditForm(request.POST)

        # Check if the form is valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)
            customer_instance.street_address_1 = form.cleaned_data['street_address_1']
            customer_instance.street_address_2 = form.cleaned_data['street_address_2']
            customer_instance.city = form.cleaned_data['city']
            customer_instance.state = form.cleaned_data['state']
            customer_instance.zip_code = form.cleaned_data['zip_code']
            customer_instance.save()

            # redirect to a new URL:
            return HttpResponseRedirect(reverse('home'))

    # If this is a GET (or any other method) create the default form.
    else:
        form = CustomerEditForm()

    context = {
        'form': form,
        'customer_instance': customer_instance,
    }

    return render(request, 'registration/edit_customer.html', context)