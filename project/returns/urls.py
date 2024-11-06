from django.urls import path
from . import views

urlpatterns = [
    path('return/', views.return_product, name='return_product'),  # Return form page
    path('success/', views.return_success, name='return_success'),  # Success page
]
