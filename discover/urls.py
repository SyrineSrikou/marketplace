from django.urls import path
from . import views

app_name = 'discover'

urlpatterns = [
    path('', views.home, name='home'),
    path('product/<slug:category_slug>/<slug:product_slug>', views.product_detail, name='product_detail'), 

    path('discover/', views.discoverPage, name='discover_page'),
    path('search/', views.search, name='search'),
    path('discover/category/<slug:category_slug>/', views.category, name ='category'),
    path('category/<slug:category_slug>/', views.products_by_category, name ='products_by_category'),

]