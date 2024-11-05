from django.urls import path

from . import views

app_name = "store"


urlpatterns = [
    
    path("products/", views.search_product,name="product_search"),
    path('cart/', views.cart_view, name='cart_view'),
    path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('process_payment/', views.process_payment, name='process_payment'),
]