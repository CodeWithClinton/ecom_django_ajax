from django.urls import path
from . import views

urlpatterns = [
    path('', views.store, name = 'store'),
    path('cart', views.cart, name = 'cart'),
    path('checkout', views.checkout, name = 'checkout'),
    path('updatecart', views.updateCart),
    path('updatequantity', views.updateQuantity),
    path('payment', views.payment, name = 'payment')
]