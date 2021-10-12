from django.urls import path
from . import views


app_name = 'cart'


urlpatterns = [
    path('cart/', views.cart_detail, name='cart_detail'),
    path('cart/checkout/', views.place_order, name='place_order'),
    path('checkout_complete/<int:order_id>', views.checkout_complete, name='checkout_complete'),


]