from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('profile/', views.edit_profile, name='edit_profile'),

    path('addresses/', views.addresses, name='addresses'),
    path("add_address/", views.add_address, name="add_address"),
    path("addresses/edit/<slug:id>/", views.edit_address, name="edit_address"),
    path("addresses/delete/<slug:id>/", views.delete_address, name="delete_address"),
    path("addresses/set_default/<slug:id>/", views.set_default, name="set_default"),


    # Wish List
    path("wishlist", views.wishlist, name="wishlist"),
    path("wishlist/add_to_wishlist/<int:id>", views.add_to_wishlist, name="user_wishlist"),

    path('stores/', views.stores, name='stores'),
    path('store/<slug:slug>/products', views.store_products, name='store_products'),
    path('store/<slug:slug>/orders', views.store_orders, name='store_orders'),
    path('store/<slug:slug>/orders/<int:order_id>', views.store_order_details, name='store_order_details'),
    path('store/<slug:slug>/orders/<int:order_id>/accept_order', views.accept_order, name='accept_order'),  
    path('store/<slug:slug>/orders/<int:order_id>/order_completed', views.order_completed, name='order_completed'),  
    path('store/<slug:slug>/orders/<int:order_id>/order_canceled', views.order_canceled, name='order_canceled'),  


    #user orders
    path('orders/', views.orders, name='orders'),
    path('orders/order/<int:order_id>', views.order_details, name ='user_order_details'),


   
]