
from django.contrib import admin
from .models import Store, Product, ProductImage, ReviewRating
import admin_thumbnails

@admin_thumbnails.thumbnail('image')
class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price','stock' ,'category', 'store' , 'added_by', 'created_date','is_available' )
    prepopulated_fields = {'slug': ('name',)}
    inlines = [ProductImageInline]

admin.site.register(Store)
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductImage)
admin.site.register(ReviewRating)

