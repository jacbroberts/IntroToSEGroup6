# returns/models.py
from django.db import models

class ProductReturn(models.Model):
    order_id = models.CharField(max_length=20)
    product_name = models.CharField(max_length=100)
    return_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Return for order {self.order_id} - {self.product_name}"
