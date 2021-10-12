from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('blog/', views.blog, name='blog'),
    path('blog/<slug:blogpost>/', views.blogpost, name='blogpost'),
    path('like/<slug:blogpost>',views.like, name = 'like'),
    path('comment/<slug:blogpost>',views.add_comment, name = 'add_comment'),



]