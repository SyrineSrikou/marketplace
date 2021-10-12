from django.http.response import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404, reverse
from store.forms import CreateStoreForm, ProductForm, ReviewForm
from store.models import Store, Product, ProductImage, ReviewRating
from django.shortcuts import render
from django.utils.text import slugify
from django.contrib.auth.models import Group
from django.contrib import messages
from django.contrib.auth.decorators import login_required


# Create your views here.



# Open a Store
@login_required(login_url='accounts:login')

def createStore(request):
    store=Store.objects.filter(owner=request.user)
    user = request.user
    form = CreateStoreForm()
    if request.method == 'POST':
        form = CreateStoreForm(request.POST, request.FILES)
        if form.is_valid():
            store = form.save(commit=False)
            store.owner= user
            store.slug = slugify(store.name)
            store.save()
            form.save()
            store = form.cleaned_data.get('name')

            return redirect('dashboard:stores')

    context = {'form':form, 'store':store}
    return render(request, 'create_store.html', context)


@login_required(login_url='accounts:login')
def edit_store(request, slug):
    store = Store.objects.get(owner=request.user, slug=slug)
    if request.method == 'POST':
        form = CreateStoreForm(request.POST, request.FILES, instance=store)
        
        if form.is_valid():
            form.save()

            return redirect('dashboard:stores', store.slug)
    else:
        form = CreateStoreForm(instance=store)
    
    return render(request, 'edit_store.html', {'form': form, 'store': store})

@login_required(login_url='accounts:login')
def delete_store(request,slug):
    store = Store.objects.get(owner=request.user, slug=slug).delete()
    return redirect("dashboard:stores")


#get specific store
@login_required(login_url='accounts:login')

def store(request, slug):
    store = Store.objects.get(owner=request.user, slug=slug)
    context = {
        'store' : store
    }
    return render(request, 'store_dashboard.html', context)





@login_required(login_url='accounts:login')

def add_product(request, slug):
    store = get_object_or_404(Store, slug=slug)

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.added_by = request.user
            product.store = store
            product.slug = slugify(product.name)
            product.save()
            images = request.FILES.getlist("more_images")
            for i in images:
                ProductImage.objects.create(product=product, image=i)

            return redirect('dashboard:store_products', store.slug)
    else:
        form = ProductForm()
    
    return render(request, 'add_product.html', {'form': form,  'store':store})



@login_required(login_url='accounts:login')
def edit_product(request, product_slug):
    store = Store.objects.get(owner=request.user)
    product = Product.objects.filter(store=store, slug=product_slug).first()
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        
        if form.is_valid():
            form.save()

            return redirect('dashboard:store_products', store.slug)
    else:
        form = ProductForm(instance=product)
    
    return render(request, 'edit_product.html', {'form': form, 'product': product , 'store':store})

@login_required(login_url='accounts:login')
def delete_product(request,product_slug):
    store = Store.objects.get(owner=request.user)
    product = Product.objects.filter(store=store, slug=product_slug).delete()
    return redirect("dashboard:store_products", store.slug)



@login_required(login_url='accounts:login')
def submit_review(request,  category_slug, product_slug):
    url = request.META.get('HTTP_REFERER')
    product = get_object_or_404(Product, category__slug=category_slug, slug=product_slug)

    if request.method == 'POST':
        try:
            reviews = ReviewRating.objects.get(user__id=request.user.id, product__id=product.id)
            form = ReviewForm(request.POST, instance=reviews)
            form.save()
            messages.success(request, 'Thank you! Your review has been updated.')
            return redirect(url)
        except ReviewRating.DoesNotExist:
            form = ReviewForm(request.POST)
            if form.is_valid():
                data = ReviewRating()
                data.subject = form.cleaned_data['subject']
                data.rating = form.cleaned_data['rating']
                data.review = form.cleaned_data['review']
                data.product_id = product.id
                data.user_id = request.user.id
                data.save()
                messages.success(request, 'Thank you! Your review has been submitted.')
                return redirect(url)




def all_stores(request):
    stores = Store.objects.all()

    return render(request, 'all_stores.html', {'stores': stores})

def single_store(request, slug):
    single_store = get_object_or_404(Store, slug=slug)
    sproducts = Product.objects.filter(store=single_store)
    return render(request, 'single_store.html', {'single_store': single_store, 'sproducts':sproducts})


