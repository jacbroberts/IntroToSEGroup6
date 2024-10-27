from django.urls import path

from .views import SignUpView, edit_seller, edit_customer, make_customer, make_seller

app_name = "accounts"

urlpatterns = [
    path("signup/", SignUpView.as_view(), name="signup"),
    path("edit_seller/", edit_seller , name="seller_edit"),
    path("edit_customer/", edit_customer, name="customer_edit"),
    path("create_seller/",make_seller, name="create_seller"),
    path("create_customer/", make_customer, name="create_customer")

]