from django.urls import path
from adminshop import views

app_name = 'adminshop'
urlpatterns = [
    path('login_admin/', views.loginAdmin.as_view(), name='login-admin'),
    path('', views.index, name='index'),
    path('categories/', views.admin_categories, name='categories'),
    path('add_category/', views.add_category, name='add_category'),
    #path('category/<slug:category_slug>/update', views.updateCategory, name="update_category"),
    #path('categories/delete_category/<slug:category_slug>', views.delete_category, name="delete_category"),


    path('users/', views.users, name='users'),
    path('business_users/', views.business_users, name='business_users'),
    path('stores/', views.admin_stores, name='admin_stores'),
    path('admin_store_details/<slug:slug>', views.admin_store_details, name='admin_store_details'),
    path('admin_stores/<slug:slug>/delete', views.admin_delete_store, name='admin_delete_store'),
    path('staff_stores/', views.staff_stores, name='staff_stores'),
    path('admin_stores/', views.approve_store, name='approve_store'),
    path('approve_store/<slug:slug>', views.approve_store, name='approve_store'),  
    path('reject_store/<slug:slug>', views.reject_store, name='reject_store'),  
    path('orders/', views.admin_orders, name='admin_orders'),
    path('products/', views.products, name='products'),

    path('tickets/', views.supportTickets, name='support_tickets'),
    path('tickets/ticket/<int:ticket_id>', views.support_single_ticket, name='support_single_ticket'),
    path('tickets/ticket/<int:ticket_id>/close', views.close_ticket, name='close_ticket'),


    #Staff User
    path('support_create',views.StaffUserCreateView.as_view(),name="support_create"),
    path('support_users',views.support_users,name="support_users"),
    path("support_users/delete/<int:pk>/", views.delete_support, name="delete_support"),

    path('bloglist',views.bloglist,name="bloglist"),
    path("blog/add_blogpost", views.add_blogpost, name="add_blogpost"),
    path("bloglist/delete/<int:pk>/", views.featured_post, name="featured_post"),
    path("bloglist/delete/<int:pk>/", views.delete_blogpost, name="delete_blogpost"),



]

