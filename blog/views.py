from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render, get_object_or_404
from django.http import JsonResponse
from django.urls.base import reverse
from django.contrib.auth.decorators import login_required
from .forms import CommentForm
from .models import BlogPost, Comment
from django.contrib import messages


def blog(request):
    blogposts = BlogPost.objects.order_by('-publish') 
    context ={
        'blogposts' : blogposts
    }
    return render(request, 'blog.html', context)

def blogpost(request, blogpost):
    
    blogpost = get_object_or_404(BlogPost, slug=blogpost)
    featuredblogposts = BlogPost.objects.all()[0:3]

    total_likes = blogpost.total_likes()
    
    liked = False
    if blogpost.likes.filter(id=request.user.id).exists():
        liked = True

    comments = Comment.objects.filter(blogpost=blogpost.id )
    context = {
        'blogpost': blogpost,
        'featuredblogposts': featuredblogposts,
        'total_likes':total_likes,
        'liked':liked,
        'comments':comments,

    }

    return render(request, 'blogpost.html', context)

@login_required(login_url='accounts:login')
def like(request, blogpost):
    blogpost = get_object_or_404(BlogPost, slug=blogpost)
    liked = False
    if blogpost.likes.filter(id=request.user.id).exists():
        blogpost.likes.remove(request.user)
        liked = False

    else:
        blogpost.likes.add(request.user)
        liked = True

    return redirect('blog:blogpost', blogpost.slug)




@login_required(login_url='accounts:login')
def add_comment(request, blogpost):

    url = request.META.get('HTTP_REFERER')
    blogpost = get_object_or_404(BlogPost, slug=blogpost)

    if request.method == 'POST':
        try:
            comments = Comment.objects.get(user__id=request.user.id, blogpost__id=blogpost.id)
            form = CommentForm(request.POST, instance=comments)
            form.save()
            messages.success(request, 'Thank you! Your comment has been updated.')
            return redirect(url)
        except Comment.DoesNotExist:
            form = CommentForm(request.POST)
            if form.is_valid():
                data = Comment()
                data.user = request.user
                data.comment = form.cleaned_data['comment']
                data.blogpost = blogpost
                data.save()
                messages.success(request, 'Thank you! Your comment has been submitted.')
                return redirect(url)


