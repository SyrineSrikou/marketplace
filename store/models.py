from django.db import models
from django.db.models.fields import BooleanField
from discover.models import Category
from django.urls import reverse
from accounts.models import User

from io import BytesIO
from PIL import Image

from django.core.files import File
from django.db import models
from django.db.models import Avg, Count


# Create your models here.

Pending = 0
Opened = 1 
Rejected =2

STORE_STATUS = (
    ("Pending", "Pending"),
    ("Opened", "Opened"),
    ("Rejected", "Rejected"),
)

class Store(models.Model):
    owner          = models.ForeignKey(User, on_delete=models.CASCADE)
    name           = models.CharField(max_length=200)
    slug           = models.SlugField(max_length=200, unique=True)
    logo           = models.ImageField(blank=True, upload_to='images/stores/logos')
    phone_number   = models.CharField(max_length=50)
    description    = models.TextField()
    trader_license = models.ImageField(upload_to='images/stores/licenses',default='', blank=True)
    city           = models.CharField(max_length=200)
    address        = models.CharField(max_length=200)
    create_date    = models.DateTimeField(auto_now_add=True)
    is_approved    = models.BooleanField(default=False)
    store_status   = models.CharField(max_length=50, default="Pending", choices=STORE_STATUS)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name
    
    def get_balance(self):
        items = self.items.filter(store_paid=False, order__stores__in=[self.id])
        return sum((item.product.price * item.quantity) for item in items)
    
    def get_paid_amount(self):
        items = self.items.filter(store_paid=True, order__stores__in=[self.id])
        return sum((item.product.price * item.quantity) for item in items)


class Product(models.Model):
    name            = models.CharField(max_length=200, unique=True)
    slug            = models.SlugField(max_length=200, unique=True)
    description     = models.TextField(max_length=500, blank=True)
    price           = models.IntegerField()
    image         = models.ImageField(upload_to='images/products')
    stock           = models.IntegerField()
    is_available    = models.BooleanField(default=True)
    is_featured     = models.BooleanField(default=False)
    is_digital      = models.BooleanField(default=False)
    category        = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_date    = models.DateTimeField(auto_now_add=True)
    modified_date   = models.DateTimeField(auto_now=True)
    store           = models.ForeignKey(Store, on_delete=models.CASCADE)
    added_by        = models.ForeignKey(User, on_delete=models.CASCADE)
    return_policy = models.CharField(max_length=300, null=True, blank=True)
    thumbnail = models.ImageField(upload_to='uploads/', blank=True, null=True)

    users_wishlist = models.ManyToManyField(User, related_name="user_wishlist", blank=True)

    class Meta:
        ordering = ['-created_date']
    
    def get_thumbnail(self):
        if self.thumbnail:
            return self.thumbnail.url
        else:
            if self.image:
                self.thumbnail = self.make_thumbnail(self.image)
                self.save()

                return self.thumbnail.url
            else:
                return 'https://via.placeholder.com/240x180.jpg'
    
    def make_thumbnail(self, image, size=(300, 200)):
        img = Image.open(image)
        img.convert('RGB')
        img.thumbnail(size)

        thumb_io = BytesIO()
        img.save(thumb_io, 'JPEG', quality=85)

        thumbnail = File(thumb_io, name=image.name)

        return thumbnail

    def get_url(self):
        return reverse('product_detail', args=[self.category.slug, self.slug])

    def __str__(self):
        return self.name

    def averageReview(self):
        reviews = ReviewRating.objects.filter(product=self, status=True).aggregate(average=Avg('rating'))
        avg = 0
        if reviews['average'] is not None:
            avg = float(reviews['average'])
        return avg

    def countReview(self):
        reviews = ReviewRating.objects.filter(product=self, status=True).aggregate(count=Count('id'))
        count = 0
        if reviews['count'] is not None:
            count = int(reviews['count'])
        return count


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="products/images/")

    def __str__(self):
        return self.product.name

    

class ReviewRating(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.CharField(max_length=100, blank=True)
    review = models.TextField(max_length=500, blank=True)
    rating = models.FloatField()
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.subject
