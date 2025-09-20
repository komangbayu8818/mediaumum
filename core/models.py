from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField
from ckeditor.fields import RichTextField
from taggit.managers import TaggableManager
from taggit.models import TagBase, GenericTaggedItemBase

class Kategori(models.Model):
    judul = models.CharField(max_length=100)
    slug_kat = models.SlugField(editable=False, blank=True)

    def save(self, *args, **kwargs):
        self.slug_kat = slugify(self.judul)
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.judul

# Tag dengan counter sendiri
class ArticleTag(TagBase):
    view_count  = models.PositiveIntegerField(default=0)
    share_count = models.PositiveIntegerField(default=0)

# Tabel penghubung untuk Article <-> ArticleTag
class TaggedArticle(GenericTaggedItemBase):
    tag = models.ForeignKey(
        ArticleTag,
        related_name="tagged_items",   # ✅ penting
        on_delete=models.CASCADE,
    )

class Article(models.Model):

    judul = models.CharField(max_length=400)
    isi = RichTextField(blank=True, null=True)
    view_count = models.PositiveBigIntegerField(default=0, editable=False)
    share_count = models.PositiveBigIntegerField(default=0, editable=False)
    slug_art = models.SlugField(editable=False, blank=True, max_length=400)
    kategori = models.ForeignKey(Kategori, on_delete=models.CASCADE)
    tags = TaggableManager(through=TaggedArticle, blank=True)          # ⬅️ taggit
    thumbnail = CloudinaryField('Thumbnail', null=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, editable=False)
    pubdate = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)
    type = models.CharField(max_length=100, blank=True, default='Normal')
    status = models.CharField(max_length=20, blank=True, null=True)
    # status = models.CharField(max_length=1, choices=POST_CHOICES, default='D', blank=True)

    def save(self, *args, **kwargs):
        self.slug_art = slugify(self.judul)
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.judul

class PaidArticle(models.Model):

    judul = models.CharField(max_length=400)
    isi = RichTextField(blank=True, null=True)
    view_count = models.PositiveBigIntegerField(default=0, editable=False)
    share_count = models.PositiveBigIntegerField(default=0, editable=False)
    slug_art = models.SlugField(editable=False, blank=True, max_length=400)
    kategori = models.ForeignKey(Kategori, on_delete=models.CASCADE)
    tags = TaggableManager(through=TaggedArticle, blank=True)          # ⬅️ taggit
    thumbnail = CloudinaryField('Thumbnail', null=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, editable=False)
    pubdate = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=20, blank=True, null=True)
    type = models.CharField(max_length=100, blank=True, default='Normal')
    duration = models.IntegerField(max_length=365)
    # status = models.CharField(max_length=1, choices=POST_CHOICES, default='D', blank=True)

    def save(self, *args, **kwargs):
        self.slug_art = slugify(self.judul)
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.judul
    
class IklanRedirect(models.Model):

    judul = models.CharField(max_length=100)
    durasi = models.IntegerField(max_length=365)
    ads_potrait = CloudinaryField('Thumbnail', null=True, blank=True)
    ads_landscape = CloudinaryField('Thumbnail', null=True, blank=True)

