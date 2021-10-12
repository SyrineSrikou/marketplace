from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('marketplaceadmin/', include('adminshop.urls')),
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls', namespace='accounts')),
    path('', include('discover.urls', namespace='discover')),
    path('', include('store.urls', namespace='store')),
    path('', include('cart.urls', namespace='cart')),
    path('', include('order.urls', namespace='order')),
    path('', include('dashboard.urls', namespace='dashboard')),
    path('', include('blog.urls', namespace='blog')),
    path('', include('notifications.urls', namespace='notifications')),
    path('', include('support.urls', namespace='support')),



    path('ckeditor/', include('ckeditor_uploader.urls')),



]
 
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)