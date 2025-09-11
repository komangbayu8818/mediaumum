from django.contrib import admin
from django.urls import path, re_path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls', namespace = 'core')),
    path("tinymce/", include("tinymce.urls")),
    path('user/', include('user.urls', namespace = 'user')),
]
