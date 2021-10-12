from notifications import views
from django.urls import path

from .views import notifications

app_name = 'notifications'

urlpatterns = [
    path('notifications', views.notifications, name='notifications'),
]