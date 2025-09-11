from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth.models import User
from ckeditor.widgets import CKEditorWidget

class FormTambahArtikel(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['judul', 'isi', 'kategori', 'thumbnail']
        