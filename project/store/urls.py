from django.urls import path

from . import views

app_name = "store"


urlpatterns = [
    
    path("products/", views.search_product,name="product_search"),
    path('cart/', views.cart_view, name='cart_view'),
    path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('process_payment/', views.process_payment, name='process_payment'),
    path('validate_payment/', views.validate_payment, name='validate_payment'),
    path("sold/", views.sold_products, name="sold_products"),
    path("sold/remove/<int:item_id>/", views.processed_product, name='remove_from_sold'),
    path("add_product/", views.add_product,name="add_product"),
    path('cart/increase/<int:item_id>/', views.increase_quantity, name='increase_quantity'),
    path('cart/decrease/<int:item_id>/', views.decrease_quantity, name='decrease_quantity'),
    path('bought/',views.view_bought,name="view_bought")
]
