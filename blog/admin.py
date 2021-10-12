from django.contrib import admin
from . import models


admin.site.register(models.Tag)
admin.site.register(models.Comment)


@admin.register(models.BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('headline', 'slug', 'publish')
    prepopulated_fields = {'slug': ('headline',), }
