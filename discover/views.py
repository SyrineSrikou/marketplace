from django.http.response import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect, HttpResponseRedirect
from store.models import Product, ReviewRating, ProductImage
from order.models import OrderItem
from .models import Category
import random
from django.db.models import Q
from .forms import AddToCartForm
from django.contrib import messages
from cart.cart import Cart
from blog.models import BlogPost
from .forms import SearchForm
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

# Create your views here.
def home(request):
    products = Product.objects.all()[0:8]
    featuredblogposts = BlogPost.objects.all()[0:3]
    categories = Category.objects.all()
    featuredproducts = Product.objects.filter(is_featured=True)


    reviews = None
    for product in products:
        reviews = ReviewRating.objects.filter(product_id=product.id, status=True)

        
    context = {
        'products': products,
        'featuredblogposts': featuredblogposts,
        'reviews': reviews,
        'categories':categories,
        'featuredproducts':featuredproducts

    }


    return render(request, 'home.html', context)


def product_detail(request, category_slug, product_slug):
    
    cart = Cart(request)

    product = get_object_or_404(Product, category__slug=category_slug, slug=product_slug)


    if request.method == 'POST':
        form = AddToCartForm(request.POST)

        if form.is_valid():
            quantity = form.cleaned_data['quantity']

            cart.add(product_id=product.id, quantity=quantity, update_quantity=False)

            messages.success(request, 'The product is added successfully to the cart')

            return redirect('discover:product_detail' , category_slug=category_slug, product_slug=product_slug)
    else:
        form = AddToCartForm()


    if request.user.is_authenticated:
        try:
            orderitem = OrderItem.objects.filter(user=request.user, product_id=product.id).exists()
        except OrderItem.DoesNotExist:
            orderitem = None
    else:
        orderitem = None

    # Get the reviews
    reviews = ReviewRating.objects.filter(product_id=product.id, status=True)

    product_gallery = ProductImage.objects.filter(product_id=product.id)

    context = {
        'form': form, 
        'product': product,
        'orderitem':orderitem, 
        'reviews': reviews,
        'product_gallery': product_gallery


    }
    return render(request, 'product.html', context)

def discoverPage(request):
    
    price_from=request.GET.get('price_from', 0)
    price_to=request.GET.get('price_to', 500)

    discover_products = Product.objects.all().filter(price__gte=price_from).filter(price__lte=price_to)
    categories = Category.objects.all()
    

    paginator = Paginator(discover_products,3)
    page = request.GET.get('page')
    paged_products = paginator.get_page(page)

    context = {
        'discover_products': paged_products,
        'price_from':price_from,
        'price_to':price_to
        
    }

    return render(request, 'discover.html', context)


def search(request):
    if request.method == 'POST': # check post
        form = SearchForm(request.POST)
        if form.is_valid():
            query = form.cleaned_data['query'] # get form input data
            products=Product.objects.filter(name__icontains=query)  #SELECT * FROM product WHERE title LIKE '%query%'
            context = {'products': products, 'query':query}
            return render(request, 'search_products.html', context)

    return HttpResponseRedirect('/')


#Get products by category
def category(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug)
    category_products = Product.objects.filter(category=category)
    return render(request, 'category.html', {'category':category, 'category_products':category_products})


def products_by_category(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug)
    cproducts = Product.objects.filter(category=category)
    return render(request, 'products_category.html', {'category':category, 'cproducts':cproducts})

