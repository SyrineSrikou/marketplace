from notifications.utilities import create_notification
from support.models import ConversationMessage, Ticket
from discover.views import category
from django.contrib import auth, messages
from django.shortcuts import render,reverse, redirect, get_object_or_404
from django.views.generic import CreateView
from django.views import View
from django.utils.text import slugify
from accounts.models import User
from accounts.models import UserProfile
from django.contrib.auth import authenticate, login
from django.contrib.auth import decorators
from order.models import Order
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from accounts.models import User
from store.models import Category,Store, Product
from .forms import *
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth import get_user_model

User = get_user_model()

class loginAdmin(View):
    def get(self, request):
        return render(request, 'login-admin.html')

    def post(self, request):
        user_name = request.POST.get('username')
        pass_word = request.POST.get('password')
        my_user = authenticate(username=user_name, password=pass_word)
        if my_user is None or my_user.is_staff == 0:  # if there is no my_user in the user of django
            err = 'this space is private for only Admin & stuff'
            return render(request, 'login-admin.html', {'err': err})

        login(request, my_user)  # check login and switch pages
        return redirect('adminshop:index')


@decorators.login_required(login_url = '/marketplaceadmin/login-admin')
def logout(request):
    auth.logout(request)
    messages.success(request, 'You are logged out.')
    return redirect('adminshop:login-admin')


@decorators.login_required(login_url='/marketplaceadmin/login_admin')
def index(request):
    return render(request, 'index.html')

@decorators.login_required(login_url='/marketplaceadmin/login_admin')
def admin_categories(request):
    categories = Category.objects.all()
    return render(request, 'admin_categories.html', {'categories': categories})

@decorators.login_required(login_url='/marketplaceadmin/login_admin')
def add_category(request):

    if request.method == 'POST':
        form = CategoryForm(request.POST, request.FILES)
        if form.is_valid():
            category = form.save(commit=False)
            category.slug = slugify(category.category_name)
            category.save()
            return redirect('adminshop:categories')
    else:
        form = CategoryForm()

    return render(request, 'add_category.html', {'form': form})



def updateCategory(request, category_slug):

	category = Category.objects.get(slug=category_slug)
	form = CategoryForm(instance=category)

	if request.method == 'POST':
		form = CategoryForm(request.POST, instance=category)
		if form.is_valid():
			form.save()
			return redirect('adminshop:categories')

	context = {'form':form}
	return render(request, 'add_category.html', context)
 

def delete_category(request, category_slug):
    category = Category.objects.get(slug=category_slug).delete()
    return redirect("adminshop:categories")



@decorators.login_required(login_url='/marketplaceadmin/login_admin')
def users(request):
    users = User.objects.all()
    users_profiles = UserProfile.objects.all()

    return render(request, 'users.html', {'users': users, 'users_profiles': users_profiles})

@decorators.login_required(login_url='/marketplaceadmin/login_admin')
def business_users(request):
    users = User.objects.all().filter(is_businessuser=True)
    users_profiles = UserProfile.objects.all()
    
    for user in users: 
        user = user
        
        store = Store.objects.get(owner=user)

    return render(request, 'businessUsers.html', {'users': users, 'users_profiles': users_profiles, 'store':store})


@decorators.login_required(login_url='/marketplaceadmin/login_admin')
def admin_stores(request):
    stores = Store.objects.all()
    return render(request, 'admin_stores.html', {'stores': stores})

@decorators.login_required(login_url='/marketplaceadmin/login_admin')
def admin_store_details(request, slug):
    store =get_object_or_404(Store, slug=slug)
    context = {
        'store' : store
    }
    return render(request, 'admin_store_details.html', context)

@decorators.login_required(login_url='/marketplaceadmin/login_admin')
def admin_delete_store(request,slug):
    store = Store.objects.get(slug=slug).delete()
    return redirect("adminshop:admin_stores")


@decorators.login_required(login_url='/marketplaceadmin/login_admin')
def staff_stores(request):
    stores = Store.objects.all()
    for store in stores:
        store_status = store.store_status
        print(store_status)
        if store_status == "Pending":
            pending_stores = store
            print(pending_stores)
        elif store_status == "Opened":
            opened_stores = store
            print(opened_stores)

    return render(request, 'staff_stores.html',
                  {'stores': stores, ' pending_stores': pending_stores, 'opened_stores': opened_stores})


#approve store creation request 
@decorators.login_required(login_url='/marketplaceadmin/login_admin')
def approve_store(request, slug):
    store = Store.objects.get(slug=slug)
    store.is_approved = True
    store.store_status = 'Opened'
    store.save()
    user = store.owner
    user.is_businessuser = True
    group = Group.objects.get_or_create(name='businessusers') 
    user.groups.add(group[0])
    user.save()
   

    return redirect('adminshop:admin_stores') 

@decorators.login_required(login_url='/marketplaceadmin/login_admin')
def reject_store(request, slug):
    store = Store.objects.get(slug=slug)
    store.is_approved = False
    store.store_status = 'Rejected'
    store.save()
    

    return redirect('adminshop:admin_stores') 

@decorators.login_required(login_url='/marketplaceadmin/login_admin')
def products(request):
    products = Product.objects.all().order_by('created_date')
    return render(request, 'admin_products.html', {'products': products})

@decorators.login_required(login_url='/marketplaceadmin/login_admin')
def admin_orders(request):
    orders = Order.objects.all()
    return render(request, 'admin_orders.html', {'orders': orders})



@decorators.login_required(login_url='/marketplaceadmin/login_admin')
def supportTickets(request):
    tickets = Ticket.objects.all().order_by('-create_date')
    return render(request, 'support_tickets.html', {'tickets': tickets})



    
@decorators.login_required(login_url='/marketplaceadmin/login_admin')
def support_single_ticket(request, ticket_id):
    
    ticket = get_object_or_404(Ticket, pk=ticket_id)
    
     
    if request.method == 'POST':
        content = request.POST.get('content')

        if content:
            conversationmessage = ConversationMessage.objects.create(ticket=ticket, content=content, created_by=request.user)
            create_notification(request, ticket.created_by, 'message', extra_id=ticket.id)

            return redirect('adminshop:support_single_ticket', ticket_id=ticket_id)
    
    
    context = {
        'ticket' : ticket
    }
    return render(request, 'support_single_ticket.html', context)
   

def close_ticket(request,ticket_id ):
    ticket = get_object_or_404(Ticket, pk=ticket_id)
    ticket.status = 'Closed'
    ticket.save()
    return redirect('adminshop:support_tickets')



class StaffUserCreateView(SuccessMessageMixin,CreateView):
    template_name="add_support.html"
    model=User
    fields=["first_name","last_name","email","username","password"]

    def form_valid(self,form):

        #Saving Custom User Object for staff User
        user=form.save(commit=False)
        user.is_active=True
        user.is_staff = True
        user.save()
        group = Group.objects.get_or_create(name='support') 
        user.groups.add(group[0])
        user.set_password(form.cleaned_data["password"])
        user.save()
        # Create a user profile
        profile = UserProfile()
        profile.user_id = user.id
        profile.profile_picture = '/users/images/user.png'
        profile.save()
            

        messages.success(self.request,"Staff User Created")
        return HttpResponseRedirect(reverse("adminshop:support_users"))


def is_support(User):
    return User.groups.filter(name='support').exists()


@decorators.login_required(login_url='/marketplaceadmin/login_admin')
def support_users(request):
        support_users = User.objects.all().filter(is_staff=True).filter(is_admin=False)
        print(support_users)
        users_profiles = UserProfile.objects.all()
     
        return render(request, 'supportUsers.html', {'support_users': support_users, 'users_profiles': users_profiles})


@decorators.login_required(login_url='/marketplaceadmin/login_admin')
def delete_support(request,pk):
    support = User.objects.filter(id=pk).delete()
    return redirect("adminshop:support_users")

#Blog
def add_blogpost(request):

    
    if request.method == 'POST':
        form = BlogPostForm(request.POST, request.FILES)
        if form.is_valid():
            blogpost = form.save(commit=False)
            blogpost.slug = slugify(blogpost.headline)
            blogpost.save()
           
            return redirect('adminshop:bloglist')
    else:
        form = BlogPostForm()
    

    return render(request, 'admin_add_blogpost.html', {'form':form})



def bloglist(request):
    blogposts = BlogPost.objects.all()
    return render(request, 'admin_blog_list.html', {'blogposts':blogposts})


@decorators.login_required(login_url='/marketplaceadmin/login_admin')
def delete_blogpost(request,pk):
    blogpost = BlogPost.objects.filter(id=pk).delete()
    return redirect("adminshop:bloglist")


def featured_post(request,id ):
    blogpost = get_object_or_404(BlogPost, pk=id)
    blogpost.is_featured = True
    blogpost.save()
    return redirect('adminshop:bloglist')
