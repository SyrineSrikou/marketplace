from django.shortcuts import render
from store.models import Product, Store
from django.shortcuts import render, reverse
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

from order.models import Order, OrderItem
from django.shortcuts import render, redirect, get_object_or_404
from accounts.forms import UserProfileForm, UserForm, UserAddressForm
from accounts.models import User, UserProfile, Address
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
# Create your views here.


@login_required(login_url='login')
def edit_profile(request):
    userprofile = get_object_or_404(UserProfile, user=request.user)
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = UserProfileForm(request.POST, request.FILES, instance=userprofile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile has been updated.')
            return redirect('dashboard:edit_profile')
    else:
        user_form = UserForm(instance=request.user)
        profile_form = UserProfileForm(instance=userprofile)
    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        'userprofile': userprofile,
    }
    return render(request, 'profile.html', context)

@login_required(login_url='accounts:login')
def addresses(request):
    addresses = Address.objects.filter(user=request.user)
    return render(request, "addresses.html", {"addresses":addresses})

@login_required(login_url='accounts:login')
def add_address(request):
    if request.method == "POST":
        address_form = UserAddressForm(data=request.POST)
        if address_form.is_valid():
            address_form = address_form.save(commit=False)
            address_form.user = request.user
            address_form.save()
            return HttpResponseRedirect(reverse("dashboard:addresses"))
    else:
        address_form = UserAddressForm()
    return render(request, "edit_addresses.html", {"form": address_form})

@login_required(login_url='accounts:login')
def edit_address(request, id):
    if request.method == "POST":
        address = Address.objects.get(pk=id, user=request.user)
        address_form = UserAddressForm(instance=address, data=request.POST)
        if address_form.is_valid():
            address_form.save()
            return HttpResponseRedirect(reverse("dashboard:addresses"))
    else:
        address = Address.objects.get(pk=id, user=request.user)
        address_form = UserAddressForm(instance=address)
    return render(request, "edit_addresses.html", {"form": address_form})


@login_required(login_url='accounts:login')
def delete_address(request, id):
    address = Address.objects.filter(pk=id, user=request.user).delete()
    return redirect("dashboard:addresses")

@login_required(login_url='accounts:login')
def set_default(request, id):
    Address.objects.filter(user=request.user, default=True).update(default=False)
    Address.objects.filter(pk=id, user=request.user).update(default=True)

    previous_url = request.META.get("HTTP_REFERER")

    if "delivery_address" in previous_url:
        return redirect("order:delivery_address")

    return redirect("dashboard:addresses")


@login_required(login_url='accounts:login')
def wishlist(request):
    products = Product.objects.filter(users_wishlist=request.user)
    return render(request, "user_wishlist.html", {"wishlist": products})

@login_required(login_url='accounts:login')
def add_to_wishlist(request, id):
    product = get_object_or_404(Product, id=id)
    if product.users_wishlist.filter(id=request.user.id).exists():
        product.users_wishlist.remove(request.user)
        messages.success(request, product.name + " has been removed from your WishList")
    else:
        product.users_wishlist.add(request.user)
        messages.success(request, "Added " + product.name + " to your WishList")
    return HttpResponseRedirect(request.META["HTTP_REFERER"])




#Get all stores by user
@login_required(login_url='accounts:login')
def stores(request):
    stores =  request.user.store_set.all()
    return render(request, 'stores.html', {'stores': stores})

@login_required(login_url='accounts:login')
def store_products(request, slug):
    user = request.user
    store = Store.objects.get(owner=user, slug=slug)

    products = Product.objects.filter(store=store)
    context = {
        'store': store,
        'products' : products
    }
    return render(request, 'store_products.html', context)


@login_required(login_url='accounts:login')
def store_orders(request, slug):
    user = request.user
    store = Store.objects.get(owner=user, slug=slug)
    orders = store.orders.all()

    for order in orders:
        order.store_amount = 0
        order.store_paid_amount = 0
        order.fully_paid = True

        for item in order.items.all():
            if item.store == store:
                if item.store_paid:
                    order.store_paid_amount += item.get_total_price()
                else:
                    order.store_amount += item.get_total_price()
                    order.fully_paid = False

    return render(request, 'store_orders.html', {'store': store, 'orders':orders })


@login_required(login_url='accounts:login')
def orders(request):
    user = request.user
    orders = user.order_set.all().order_by("-id")
    
    paginator = Paginator(orders,2)
    page = request.GET.get('page')
    paged_orders = paginator.get_page(page)
    return render(request, 'user_orders.html', {'orders': paged_orders})

@login_required(login_url='accounts:login')
def order_details(request, order_id):
    order =get_object_or_404(Order, pk=order_id)
    context = {
        'order' : order
    }
    return render(request, 'user_order_details.html', context)

@login_required(login_url='accounts:login')
def store_order_details(request,slug, order_id):
    user = request.user
    store = Store.objects.get(owner=user, slug=slug)
    order =get_object_or_404(Order, pk=order_id)
    
    order.store_amount = 0
    order.store_paid_amount = 0
    order.fully_paid = True

    for item in order.items.all():
        if item.store == store:
            if item.store_paid:
                order.store_paid_amount += item.get_total_price()
            else:
                order.store_amount += item.get_total_price()
                order.fully_paid = False
    
    context = {
       'order' : order,
        'store': store,
    }
    return render(request, 'store_order_details.html', context)


def accept_order(request,slug, order_id):
    user = request.user
    store = Store.objects.get(owner=user, slug=slug)
    order =get_object_or_404(Order, pk=order_id)

    order.status = 'Accepted'
    order.save()

    return redirect('dashboard:store_orders', store.slug)


def order_completed(request,slug, order_id):
    user = request.user
    store = Store.objects.get(owner=user, slug=slug)
    order =get_object_or_404(Order, pk=order_id)

    order.status = 'Completed'

    for item in order.items.all():
        item.ordered = True
        item.store_paid= True
        item.product.stock -= item.quantity
        item.save()
     

    order.fully_paid = True

            
    order.save()

    return redirect('dashboard:store_orders', store.slug)


def order_canceled(request,slug, order_id):
    user = request.user
    store = Store.objects.get(owner=user, slug=slug)
    order =get_object_or_404(Order, pk=order_id)

    order.status = 'Canceled'
    order.save()

    return redirect('dashboard:store_orders', store.slug)


