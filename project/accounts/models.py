from django.db import models
from django.conf import settings
# Create your models here.
class Customer(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    is_customer = models.BooleanField(default=False)
    street_address_1 = models.CharField(max_length=50, default="")
    street_address_2 = models.CharField(max_length=50, null=True)
    city = models.CharField(max_length=50, default="")
    state = models.CharField(max_length=2, default="")
    zip_code = models.CharField(max_length=5, default="")

class Seller(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    business_name = models.CharField(max_length=50, default="")
    is_seller = models.BooleanField(default=False)