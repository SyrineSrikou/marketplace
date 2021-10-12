from django.db import models
from django.utils import timezone
from django.urls import reverse
from accounts.models import User
from ckeditor_uploader.fields import RichTextUploadingField

# Create your models here.


# Create your models here.
class TimeStamp(models.Model):
	created_at = models.DateTimeField(auto_now_add = True)
	updated_at = models.DateTimeField(auto_now = True)
	user = models.ForeignKey(User,on_delete = models.CASCADE)

	class Meta:
		abstract = True


class Tag(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class BlogPost(models.Model):

    headline = models.CharField(max_length=200)
    sub_headline = models.CharField(max_length=200, null=True, blank=True)
    image = models.ImageField(upload_to="images/blog/%Y/%m/%d/")
    body = RichTextUploadingField(null=True, blank=True)
    featured = models.BooleanField(default=False)
    tags = models.ManyToManyField(Tag, blank=True)
    slug = models.SlugField(max_length=250)
    publish = models.DateTimeField(default=timezone.now)
    likes=models.ManyToManyField(User, related_name='post_likes')
    views=models.ManyToManyField(User, related_name='post_views')
    def total_likes(self):
        return self.likes.count()
    def total_views(self):
        return self.views.count()
   
    def get_absolute_url(self):
        return reverse('blog:blogpost', args=[self.slug])

    class Meta:
        ordering = ('-publish',)

    def __str__(self):
        return self.headline

    
class Comment(models.Model):
    user = models.ForeignKey(User,related_name="comments", on_delete=models.CASCADE, blank=True, null= True)
    blogpost = models.ForeignKey(BlogPost,on_delete = models.CASCADE)
    comment = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    def __str__(self):
        return self.user.username + ": " + self.comment[0:15]