from django import forms
from taggit.forms import TagField
from .models import *

class FormTambahArtikel(forms.ModelForm):
    tags = TagField(
        required=False,
        help_text=None,
        widget=forms.TextInput(attrs={
            "id": "tags-input",
            "placeholder": "Ketik tag lalu spasi/enter...",
            "class": "border rounded-lg px-4 py-2 w-full focus:outline-none focus:ring-2 focus:ring-blue-200",
        })
    )
    class Meta:
        model = Article
        fields = ['judul', 'isi', 'kategori', 'thumbnail', 'tags']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Saat EDIT, isi initial sebagai string "a, b, c"
        if self.instance and self.instance.pk:
            self.initial['tags'] = ", ".join(
                self.instance.tags.values_list("name", flat=True)
            )

class FormIklanRedirect(forms.ModelForm):
    class Meta:
        model = ''
        fields = '__all__'

class FormIklanArtikel(forms.ModelForm):
    class Meta:
        model = PaidArticle
        fields = ['judul', 'isi', 'kategori', 'duration', 'thumbnail', 'tags']