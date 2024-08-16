from django.urls import path
from .views import *
from . import views

urlpatterns = [
    path('', views.Userindex, name='home'),
    path('signin/', views.CustomerSignin, name="signin"),
    path('product_list/', views.product_list, name="product_list"),
    path('product_detail/', views.product_detail, name="product_detail"),
    path('contact-us/', views.contact, name="contact_us"),
    path('cart/', views.cart_page, name="cart"),
    path('checkout/', views.checkout_page, name="checkout"),
    path('signup/', views.CustomerSignup, name="signup")
]