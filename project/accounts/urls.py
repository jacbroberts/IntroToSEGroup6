from django.urls import path

from .views import edit_seller, edit_customer, make_customer, make_seller, signup, login, create_admin

app_name = "accounts"

urlpatterns = [
    path("signup/", signup, name="signup"),
    path("login/", login, name="login"),
    path("edit_seller/", edit_seller , name="seller_edit"),
    path("edit_customer/", edit_customer, name="customer_edit"),
    path("create_seller/",make_seller, name="create_seller"),
    path("create_customer/", make_customer, name="create_customer"),
    path("create_admin", create_admin, name="create_admin")

]