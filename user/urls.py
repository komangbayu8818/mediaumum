from django.contrib import admin
from django.urls import path, re_path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from . import views

app_name = 'user'
urlpatterns = [
    path('login/', views.login_umum, name = 'login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register_user, name='register'),
    path('profile/dashboard/', views.halaman_profil, name='halaman-profil'),
    path('profile/edit/', views.edit_profil, name='halaman-edit-profil'),
    path('profile/password/change/', views.ubah_password, name='halaman-ubah-password'),

]
