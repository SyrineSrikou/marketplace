from django import forms
from order.models import Order
from django.conf import settings
from django.contrib import messages
from django.shortcuts import get_object_or_404, render, redirect
import datetime
from django.views.generic import View
from order.utilities import checkout, notify_customer, notify_store
from .forms import CheckoutForm
from .cart import Cart
from accounts.models import Address


def cart_detail(request):
    cart = Cart(request)
    
    remove_from_cart = request.GET.get('remove_from_cart', '')
    change_quantity = request.GET.get('change_quantity', '')
    quantity = request.GET.get('quantity', 0)

    if remove_from_cart:
        cart.remove(remove_from_cart)

        return redirect('cart:cart_detail')
    
    if change_quantity:
        cart.add(change_quantity, quantity, True)

        return redirect('cart:cart_detail')

    return render(request, 'cart.html')


def checkout_complete(request,order_id):
    user = request.user
    order =get_object_or_404(Order, pk=order_id)
    return render(request, 'checkout_complete.html', { 'order' : order,})


def place_order(request):
    cart = Cart(request)
    last_id = Order.objects.count()
    current_id = int(last_id)+ 1
    address = Address.objects.get(user=request.user, default=True)
    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        
        if form.is_valid():
            
            user = request.user
            address = Address.objects.get(user=request.user, default=True)
            order_note = form.cleaned_data['order_note']

            # Generate order number
            yr = int(datetime.date.today().strftime('%Y'))
            dt = int(datetime.date.today().strftime('%d'))
            mt = int(datetime.date.today().strftime('%m'))
            d = datetime.date(yr,mt,dt)
            current_date = d.strftime("%d%m%Y") #03082021
            order_number = current_date + str(current_id)
            

            order = checkout(request, user, address,order_note,cart.get_total_cost(), order_number)

            cart.clear()

            #notify_store(order)
            #notify_customer(order)
            
            return redirect('cart:checkout_complete' ,order.id)
    
    else:
        form = CheckoutForm()

    return render(request, 'checkout.html', {'form': form, 'address':address,})

