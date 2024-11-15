from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from .models import Product, CartItem, SoldItems
from django.contrib.auth.decorators import login_required

from .forms import PaymentForm

from accounts.models import Seller, Customer
from .forms import ProductAddForm
from django.urls import reverse


# Create your views here.
def index(request):
    user = request.user
    user_type = "none"
    if user.is_authenticated:
        
        c = Customer.objects.filter(user=request.user).first()
        
        s = Seller.objects.filter(user=request.user).first()
        if c != None:
            if c.is_customer == True:
                user_type = "customer"
        if s != None:
            if s.is_seller == True:
                user_type = "seller"
        
    else:
        user = None
    return render(request, 'home.html',{'user':user,'user_type':user_type})


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

def validate_payment(request):
    
    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            # For now, we'll simply return a success message for valid data.
            return render(request,'cart/success.html')
        else:
            # If the form is invalid, render the form again with errors displayed.
            return render(request, 'cart/cart.html', {'form': form})
    else:
        # If the request method isn't POST, handle it as invalid.
        return HttpResponse("Invalid request.")

@login_required
def process_payment(request):
    if request.method == 'POST':
        cart_items = CartItem.objects.filter(user=request.user)
        for i in cart_items:
            
            SoldItems.objects.create(user=request.user,product=i.product,quantity=i.quantity,card_number=request.POST.get("card_number"),expire_date=request.POST.get("expiry_date"),cvv=request.POST.get("cvv"))
        cart_items.delete()
        return render(request,'cart/success.html')
        
    return HttpResponse("Invalid request.")

@login_required
def sold_products(request):
    sold_products = SoldItems.objects.filter(product__seller__username__contains=request.user)
    addresses = []
    for i in sold_products:
        addresses.append(Customer.objects.get(user=i.user))
    zip_list = zip(sold_products, addresses)
    return render(request,'store/sold_list.html',{'products':zip_list})

@login_required
def processed_product(request, item_id):
    #seller has shipped item
    product_item = SoldItems.objects.filter(product__seller__username=request.user).get(id=item_id)
    product_item.delete()
    return redirect('store:sold_products')


@login_required
def add_product(request):
    seller_instance = get_object_or_404(Seller, user=request.user)  # Retrieve the Seller instance

    if request.method == 'POST':
        form = ProductAddForm(request.POST, request.FILES)

        if form.is_valid():
            product_instance = Product()
            product_instance.name = form.cleaned_data['name']
            product_instance.price = form.cleaned_data['price']
            product_instance.remaining_quantity = form.cleaned_data['remaining_quantity']
            product_instance.description = form.cleaned_data['description']
            product_instance.image = form.cleaned_data['image'] if 'image' in form.cleaned_data else None
            product_instance.seller = request.user  # Assign the User instance directly

            product_instance.save()
            return HttpResponseRedirect(reverse('home'))
    else:
        form = ProductAddForm()

    context = {
        'form': form,
        'product_instance': seller_instance,
    }

    return render(request, "store/add_product.html", context)


# View to increase quantity
def increase_quantity(request, item_id):
    item = get_object_or_404(CartItem, id=item_id)
    item.quantity += 1
    item.save()
    return redirect(reverse('store:cart_view'))

# View to decrease quantity
def decrease_quantity(request, item_id):
    item = get_object_or_404(CartItem, id=item_id)
    if item.quantity > 1:
        item.quantity -= 1
        item.save()
    else:
        item.delete()  # Remove item if quantity goes below 1
    return redirect(reverse('store:cart_view'))
