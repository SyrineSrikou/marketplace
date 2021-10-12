from django.urls import path
from . import views

app_name = 'store'

urlpatterns = [
    path('create_store/', views.createStore, name='create_store'),
    path('stores/store/<slug:slug>', views.store, name='store_dashboard'),
    path('stores/store/<slug:slug>/add_product', views.add_product, name='add_product'),
    path('submit_review/<slug:category_slug>/<slug:product_slug>/', views.submit_review, name='submit_review'),
    path('all_stores/', views.all_stores, name='all_stores'),
    path('edit-product/<slug:product_slug>/', views.edit_product, name='edit_product'),
    path("products/delete/<slug:product_slug>/", views.delete_product, name="delete_product"),

    path('all_stores/single_store/<slug:slug>', views.single_store, name='single_store'),
    path('store/edit-store/<slug:slug>/', views.edit_store, name='edit_store'),
    path("stores/delete/<slug:slug>/", views.delete_store, name="delete_store"),
    
]