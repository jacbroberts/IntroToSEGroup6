from django.contrib import admin
from .models import Customer, Seller, Admin
# Register your models here.
admin.site.register(Customer)
admin.site.register(Seller)
admin.site.register(Admin)