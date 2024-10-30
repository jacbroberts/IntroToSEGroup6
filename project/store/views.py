from django.shortcuts import render
from django.http import HttpResponse
from .models import Product
from django.contrib.auth.decorators import login_required

# Create your views here.
def index(request):
    return HttpResponse("Hello, world. You're at the store index.")

def login(request):
    pass

@login_required
def product_list(request):
    products = Product.objects.all()
    return render(request, 'store/product_list.html',{'products':products})

@login_required
def search_product(request):
    search_term = request.GET.get('search')
    
    if search_term:
        products = Product.objects.filter(name__icontains=search_term)
    else:
        products = Product.objects.all()
    return render(request,'store/product_list.html',{'products':products,'query':search_term})