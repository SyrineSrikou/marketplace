from django.urls import path
from . import views

app_name = 'support'

urlpatterns = [
    #tickets
    path('tickets/', views.tickets, name='tickets'),
    path('tickets/single_ticket/<int:ticket_id>', views.single_ticket, name='single_ticket'),
    path('tickets/single_ticket/submit', views.submit_ticket, name='submit_ticket'),

]