from django.contrib import admin
from .models import *  
from unfold.admin import ModelAdmin

# Register your models here.

# Ganti nama 'list' menjadi 'model_list' agar tidak bentrok dengan fungsi Python
model_list = [Kategori, Article, PaidArticle]

for model in model_list:
    # Membuat class Admin secara dinamis yang mewarisi dari Unfold ModelAdmin
    admin_class = type(
        f"{model.__name__}Admin",  # Membuat nama class unik, cth: "KategoriAdmin"
        (ModelAdmin,),             # Mewarisi (inherits) dari ModelAdmin milik Unfold
        {}                         # Dictionary kosong untuk atribut tambahan
    )
    admin.site.register(model, admin_class)