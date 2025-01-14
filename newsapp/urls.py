from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('admin/', include("django_admin_kubi.urls")),
    path('admin/', admin.site.urls),
    path('',include('main.urls')),
    path('ckeditor/', include('ckeditor_uploader.urls')),
] 