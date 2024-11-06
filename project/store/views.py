from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Product, CartItem
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

@login_required
def cart_view(request):
    cart_items = CartItem.objects.filter(user=request.user)
    total = sum(item.total_price() for item in cart_items) if cart_items else 0
    is_empty = not cart_items.exists()
    
    context = {
        'cart_items': cart_items,
        'total': total,
        'is_empty': is_empty,
    }
    return render(request, 'cart/cart.html', context)

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart_item, created = CartItem.objects.get_or_create(user=request.user, product=product)
    
    if not created:
        cart_item.quantity += 1
    cart_item.save()
    return redirect('store:cart_view')

@login_required
def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, user=request.user)
    cart_item.delete()
    return redirect('store:cart_view')

def process_payment(request):
    if request.method == 'POST':
        # Here we would process payment details and save billing/shipping info
        # WIP *********
        return HttpResponse("Payment processed successfully.")
    return HttpResponse("Invalid request.")
