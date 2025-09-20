from django.contrib import admin
from django.urls import path, re_path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from . import views

app_name = 'core'
urlpatterns = [
    path('', views.main_page, name='home'),
    path('article/', views.daftar_artikel, name='halaman-daftar-artikel'),
    path('add/article/', views.admin_article_form, name='tambah-artikel'),
    path('dashboard/', views.admin_article_list, name='halaman-admin'),
    path('article/detail/<slug:nm_slug>', views.detail_artikel, name='halaman-detail-artikel'),
    path('hapus/<slug:nm_slug>/', views.hapus, name='hapus'),
    path('edit/<slug:nm_slug>/', views.edit, name='edit'),
    path('share/<str:platform>/<slug:a_slug>/', views.share, name='share'),
    path('ads/pay/<slug:nm_slug>/', views.ads_bayar, name='ads-bayar'),
    path('ads/pilih/', views.ads_choice, name='halaman-pilihan-iklan'),
    path('ads/article/', views.paid_ads_form, name='halaman-iklan-berbayar'),
]
