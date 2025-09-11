from django.db import models
from django.utils.text import slugify
from django.core import validators
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField
from ckeditor.fields import RichTextField
# Create your models here.

class Kategori(models.Model):
    judul = models.CharField(max_length=100,)
    slug_kat = models.SlugField(editable=False, blank=True)

    def save(self, *args, **kwargs):
        self.slug_kat = slugify(self.judul)
        return super(Kategori, self).save(*args, **kwargs)

    def __str__(self):
        return self.judul

class Article(models.Model):
    POST_CHOICES = [('D', 'Draft'), ('P','Posting Sekarang'), ('J','Jadwalkan')]

    judul = models.CharField(max_length=400)
    isi = RichTextField(blank=True, null=True)
    view_count = models.PositiveBigIntegerField(default=0, editable=False)
    slug_art = models.SlugField(editable=False, blank=True, max_length=400)
    kategori = models.ForeignKey(Kategori, on_delete=models.CASCADE)
    thumbnail = CloudinaryField('image', null=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, editable=False)
    pubdate = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)
    # status = models.CharField(max_length=100, choices=POST_CHOICES, blank=True, default='D')

    def __str__(self):
        return self.judul
    
    def save(self, *args, **kwargs):
        self.slug_art = slugify(self.judul)
        return super(Article, self).save(*args, **kwargs)