from django.contrib import admin
from .models import Product, CartItem, SoldItems

# Register your models here.
admin.site.register(Product)
admin.site.register(CartItem)
admin.site.register(SoldItems)
