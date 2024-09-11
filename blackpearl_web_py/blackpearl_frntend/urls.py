from django.urls import path
from .views import *
from . import views

urlpatterns = [
    path('', views.Userindex, name='Userindex'),
    path('logout/', views.CustomerLogout, name="logout"),
    path('signin/', views.CustomerSignin, name="signin"),
    path('product_list/', views.product_list, name="product_list"),
    path('product_detail/', views.product_detail, name="product_detail"),
    path('contact-us/', views.contact, name="contact_us"),
    path('cart/', views.my_cart, name="cart"),
    path('add_to_cart/', views.add_to_cart, name="add_to_cart"),
    path('updatecart/', views.updatecart, name="updatecart"),
    path('remove_from_cart/<int:pk>', views.remove_from_cart, name="remove_from_cart"),
    path('checkout/', views.checkout_page, name="checkout"),
    path('signup/', views.CustomerSignup, name="signup"),
]