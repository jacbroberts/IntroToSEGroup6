from django.urls import path

from . import views

app_name = "accounts"

urlpatterns = [
    path("products", views.search_product,name="product_search")
]

