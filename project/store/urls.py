from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
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
    path('remove_product/<int:item_id>/', views.remove_product, name='remove_product'),
    path("approve_user", views.unapproved_users, name="approve_user"),
    path("approve_user/<str:user_id>/", views.approve_user, name="approve_this_user")
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)