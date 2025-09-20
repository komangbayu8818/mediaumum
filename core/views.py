from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from .forms import *
from user.models import *
from cloudinary.uploader import destroy
from django.db.models import Q
from datetime import date
from urllib.parse import quote
import random as r
from django.db.models import F, Value
from django.db.models.functions import Coalesce
from django.contrib.contenttypes.models import ContentType
from django.core.paginator import Paginator
from django.http import Http404
from itertools import chain

def resolve_post_by_slug(slug):
    """
    Kembalikan (obj, form_class, kind) untuk Article atau PaidArticle berdasarkan slug.
    Prioritas: Article -> PaidArticle.
    """
    try:
        obj = Article.objects.select_related('author', 'kategori').get(slug_art=slug)
        form_cls = FormTambahArtikel         # <- ganti kalau form-mu beda
        return obj, form_cls, 'article'
    except Article.DoesNotExist:
        pass

    try:
        obj = PaidArticle.objects.select_related('author', 'kategori').get(slug_art=slug)
        # kalau punya form khusus untuk PaidArticle, set di sini:
        form_cls = FormIklanArtikel if 'FormIklanArtikel' in globals() else FormTambahArtikel
        return obj, form_cls, 'paid'
    except PaidArticle.DoesNotExist:
        raise Http404("Post tidak ditemukan")



context = {
    'navbar': 'snippets/navbar.html',
    'simple_navbar': 'snippets/simple_navbar.html',
    'footer': 'snippets/footer.html',
    'logo' : 'images/mediaumum.png',
    'burger' : 'images/hamburger.png',
    'home' : 'images/home_icon.webp',
    'moon' : 'images/moon_icon.webp',
    'user_profile' : 'images/user.webp',
    'arrow' : 'images/down_arrow.webp',
    'arrow_hover' : 'images/down_arrow_hover.webp',
    'user_profile_hover' : 'images/user_hover.webp',
    'images' : 'images/berita.webp',
    'artikel1': 'images/artikel2.webp',
    'artikel2': 'images/artikel3.webp',
    'iklan1' : 'images/iklan.jpg',
    'iklan2' : 'images/iklan2.webp',
    'tiktok': 'images/tiktok.webp',
    'instagram': 'images/instagram.webp',
    'facebook': 'images/facebook.webp',
    'add1' : 'images/illustrasi.png',
    'add2' : 'images/illustrasi2.png'
}


# Create your views here.
def main_page(request):
    
    if request.user.is_authenticated:
        data_profil, _ = Profile.objects.get_or_create(user=request.user)
    else:
        data_profil = None
    
    tags_all = ArticleTag.objects.all()
    
    tags = tags_all.order_by("-view_count")[:5]

    advertorial = PaidArticle.objects.order_by("-pubdate")[:5]
    news_main = Article.objects.filter(type = 'normal').order_by("-pubdate")[:5]
    tags_all = ArticleTag.objects.all()
    tags = tags_all.order_by("-view_count")[:5]

    view_poin, share_poin = 1, 3 
    base = (
        Article.objects.filter(status="Posted", type="Normal")
        .select_related("author", "kategori",)          
        .annotate(
            views=Coalesce(F("view_count"), Value(0)),
            shares=Coalesce(F("share_count"), Value(0)),
            score=F("views")*view_poin + F("shares")*share_poin,
        )
        .order_by("-score", "-pubdate")
        .distinct()                                   
    )

    headline = base.first()
    remaining = base.exclude(pk=headline.pk) if headline else base

    hot_news = remaining[:5]
    used_ids = [headline.id] if headline else []
    used_ids += list(hot_news.values_list("id", flat=True))

    headline2 = base.exclude(pk__in=used_ids)[:2] 

    tambahan = {
        'data':data_profil,
        "headline": headline,
        "headline2": headline2,
        "berita_sort": hot_news,
        'tags':tags,
        'ads':advertorial,
        'berita': news_main,
    }
    sumber = context
    src ={**tambahan, **sumber}

    return render(request, 'home.html', src)

def daftar_artikel(request):
    view_poin, share_poin = 1, 3  
    artikel = Article.objects.all().annotate(
            views=Coalesce(F("view_count"), Value(0)),
            shares=Coalesce(F("share_count"), Value(0)),
            score=F("views")*view_poin + F("shares")*share_poin,
        )
    tags_all = ArticleTag.objects.all()
    if request.user.is_authenticated:
        data_profil, _ = Profile.objects.get_or_create(user=request.user)
    else:
        data_profil = None
    
    kategori = request.GET.get('kategori', '')
    cari     = request.GET.get('cari', '')
    hari     = request.GET.get('hari', '')
    sort     = request.GET.get('sort', 'update_desc')

    # Search
    if cari:
        artikel = artikel.filter(
            Q(judul__icontains=cari) |
            Q(author__username__icontains=cari) |
            Q(tags__name__icontains=cari.lstrip('#'))
        )

    # Filter Kategori
    if kategori:
        artikel = artikel.filter(kategori__judul=kategori)

    # Filter By date
    if hari:
        try:
            d = date.fromisoformat(hari)
            artikel = artikel.filter(pubdate__date=d)
        except ValueError:
            pass

    artikel = artikel.distinct()

    # Sort
    if sort == 'oldest':
        artikel = artikel.order_by('pubdate')
    elif sort == 'most_popular':
        artikel = artikel.order_by('-score')
    else:  # default
        artikel = artikel.order_by('-pubdate')

    # Pagintation
    paginator   = Paginator(artikel, 5)
    page_number = request.GET.get('page')
    page_obj    = paginator.get_page(page_number)

    list_kategori = (Kategori.objects
                    .order_by('judul')
                    .values_list('judul', flat=True)
                    .distinct())

    qs = request.GET.copy()
    qs.pop('page', None)
    base_query = qs.urlencode()  #Ubah url contoh: "kategori=Teknologi&sort=viewer_desc"
    advertorial = PaidArticle.objects.order_by("-pubdate")[:5]
    sumber = context 
    add = {
        'page_obj': page_obj,
        'berita': page_obj.object_list,
        'is_paginated': page_obj.has_other_pages(),
        'tags': tags_all.order_by("-view_count")[:5],
        'list_kategori': list_kategori,
        'base_query': base_query,
        'data': data_profil,
        'ads':advertorial
    }
    src = {**sumber, **add}
    return render(request, 'daftar_artikel.html', src)


def detail_artikel(request, nm_slug):
    obj, _form_cls, kind = resolve_post_by_slug(nm_slug)
    data_profil = Profile.objects.get_or_create(user=request.user)[0] if request.user.is_authenticated else None

    
    advertorial = PaidArticle.objects.order_by("-pubdate")[:5]

    # +1 view (sekali per session/user per artikel)
    session_key = f"viewed_{getattr(request.user, 'id', 'guest')}_{obj.slug_art}"
    if not request.session.get(session_key):
        obj.__class__.objects.filter(pk=obj.pk).update(view_count=F("view_count") + 1)

        # +1 view untuk tag kalau model punya taggit & tabelnya mendukung
        if hasattr(obj, "tags"):
            ct = ContentType.objects.get_for_model(obj.__class__)
            # Jika kamu punya GenericTaggedItemBase, sesuaikan model penghubungnya:
            try:
                ArticleTag.objects.filter(
                    tagged_items__content_type=ct,
                    tagged_items__object_id=obj.pk,
                ).update(view_count=F("view_count") + 1)
            except Exception:
                pass

        request.session[session_key] = True

    sumber = context
    add = {
        'data':data_profil,
        "artikel": obj,
        "data": data_profil,
        "ads": advertorial,
        "kind": kind,
    }
    src = {**sumber, **add}
    return render(request, "detail_artikel.html", src)

def share(request, platform, a_slug):
    # ambil artikel
    a = get_object_or_404(Article, slug_art=a_slug)

    # batasi 1x per sesi per artikel+platform
    session_key = f"shared_{a_slug}_{platform}"
    if not request.session.get(session_key):
        Article.objects.filter(pk=a.pk).update(share_count=F('share_count') + 1)

        ct = ContentType.objects.get_for_model(Article)
        ArticleTag.objects.filter(
            tagged_items__content_type=ct,
            tagged_items__object_id=a.pk,
        ).update(share_count=F('share_count') + 1)

        request.session[session_key] = True

    # url absolut artikel (pakai get_absolute_url kalau ada)
    try:
        article_url = request.build_absolute_uri(a.get_absolute_url())
    except Exception:
        # fallback kalau belum punya get_absolute_url
        article_url = request.build_absolute_uri(f"/article/{a.slug_art}/")

    title = getattr(a, "judul", getattr(a, "title", "Baca artikel ini"))
    url = article_url
    m_choice = [f"""📰 BREAKING NEWS 
{title}
    
Selengkapnya baca di sini 👇
{url}

#MediaUmum #Teknologi
    """,
    f"""💡 Artikel Terbaru 
{title}
    
Klik tautan berikut untuk membaca lengkapnya:
{url}

#MediaUmum #BeritaTeknologi
    """,
    f"""🔥 Hot News 
{title}
    
Baca selengkapnya di:
{url}

    #MediaUmum #Teknologi
    """
    ]

    m_choice_wa = [
    f"""=== BREAKING NEWS ===
{title}

Selengkapnya baca di sini:
{url}

#MediaUmum #Teknologi""",

    f"""=== ARTIKEL TERBARU ===
{title}

Klik tautan berikut untuk membaca lengkapnya:
{url}

#MediaUmum #BeritaTeknologi""",

    f"""=== HOT NEWS ===
{title}

Baca selengkapnya di:
{url}

#MediaUmum #Teknologi"""
    ]

    m_wa =r.choice(m_choice_wa)
    m = r.choice(m_choice)
    m_encoded = quote(m, safe="")
    m_wa_encoded = quote(m_wa, safe="")

    # tentukan tujuan platform
    if platform == "wa":
        target = f"https://wa.me/?text={m_wa_encoded}"
    elif platform == "fb":
        target = f"https://www.facebook.com/sharer/sharer.php?u={url}"
    elif platform == "x":
        target = f"https://twitter.com/intent/tweet?text={m_encoded}"
    else:
        target = article_url  # fallback

    return redirect(target)

def ads_choice(request):
    if request.user.is_authenticated:
        data_profil, _ = Profile.objects.get_or_create(user=request.user)
    else:
        data_profil = None
    sumber = context
    add = {
        'judul1':'Klik & Redirect',
        'judul2':'Artikel Berbayar / Advertorial',
        'desc1':'Tarik trafik ke website Anda dalam hitungan detik. Ideal untuk kampanye flash sale, event, atau WhatsApp bisnis.',
        'desc2':'Ceritakan produk Anda lewat artikel yang informatif dan kredibel. Tingkatkan kepercayaan, visibilitas, dan konversi.',
        'btn1':'Mulai Redirect',
        'btn2':'Buat Advertorial',
        'ads1':'images/ads2_illustration.webp',
        'ads2':'images/ads1_illustration.webp',
        'data': data_profil
    }
    src = {**sumber, **add}
    return render(request, 'pilihan_iklan.html', src)

@login_required
def admin_article_form(request):
    if request.user.is_authenticated:
        data_profil, _ = Profile.objects.get_or_create(user=request.user)
    else:
        data_profil = None
    if request.method == "POST":
        form = FormTambahArtikel(request.POST, request.FILES)
        if form.is_valid():
            article = form.save(commit=False)
            article.author = request.user
            article.status = 'posted'
            article.save()
            form.save_m2m()
            messages.success(request, 'Artikel berhasil dipublikasikan.')
            return redirect('core:halaman-admin')
        else:
            messages.error(request, "Form tidak valid. Periksa kembali input Anda.")
    else:
        form = FormTambahArtikel()
    sumber = context
    add = {
        "form":form,
        'judul': 'Tambah Artikel',
        'data':data_profil,
    }

    src = {**sumber, **add}

    # cukup kirim context ini saja
    return render(request, "admin_form.html", src)

@login_required
def paid_ads_form(request):
    if request.user.is_authenticated:
        data_profil, _ = Profile.objects.get_or_create(user=request.user)
    else:
        data_profil = None
    if request.method == "POST":
        form = FormIklanRedirect(request.POST, request.FILES)
        if form.is_valid():
            article = form.save(commit=False)
            article.author = request.user
            article.status = 'pending'
            article.type = 'Ads'
            article.save()
            form.save_m2m()
            return redirect('core:ads-bayar', nm_slug=article.slug_art)
        else:
            messages.error(request, "Form tidak valid. Periksa kembali input Anda.")
    else:
        form = FormIklanRedirect()
    sumber = context
    add = {
        "form":form,
        'judul': 'Artikel Berbayar',
        'data':data_profil,
    }

    src = {**sumber, **add}

    # cukup kirim context ini saja
    return render(request, "iklan_artikel_form.html", src)


@login_required
def admin_article_list(request):
    # --- base queryset (kedua model) ---
    artikel = Article.objects.select_related('kategori', 'author')\
                            .filter(author=request.user)
    artikel_p = PaidArticle.objects.select_related('kategori', 'author')\
                            .filter(author=request.user)
    data_profil, _ = Profile.objects.get_or_create(user=request.user)

    # --- ambil parameter ---
    kategori = request.GET.get('kategori', '')
    cari     = request.GET.get('cari', '')
    hari     = request.GET.get('hari', '')
    sort     = request.GET.get('sort', 'update_desc')

    # --- filter yang sama untuk keduanya ---
    if cari:
        q = Q(judul__icontains=cari) | Q(author__username__icontains=cari)
        artikel   = artikel.filter(q)
        artikel_p = artikel_p.filter(q)

    if kategori:
        artikel   = artikel.filter(kategori__judul=kategori)
        artikel_p = artikel_p.filter(kategori__judul=kategori)

    if hari:
        try:
            d = date.fromisoformat(hari)
            artikel   = artikel.filter(pubdate__date=d)
            artikel_p = artikel_p.filter(pubdate__date=d)
        except ValueError:
            pass

    # --- gabungkan dua model (di Python) ---
    posts = list(chain(artikel, artikel_p))

    # --- sorting di Python (menyamakan perilaku opsi sort) ---
    def updated_at(o):
        # fallback ke pubdate kalau field update tidak ada
        return getattr(o, 'update', None) or getattr(o, 'pubdate', None)

    if sort == 'update_asc':
        posts.sort(key=updated_at)
    elif sort == 'viewer_desc':
        posts.sort(key=lambda o: getattr(o, 'view_count', 0), reverse=True)
    elif sort == 'viewer_asc':
        posts.sort(key=lambda o: getattr(o, 'view_count', 0))
    else:  # 'update_desc' default
        posts.sort(key=updated_at, reverse=True)

    # --- data tambahan ---
    list_kategori = (Kategori.objects.order_by('judul')
                    .values_list('judul', flat=True).distinct())
    data_profil, _ = Profile.objects.get_or_create(user=request.user)

    sumber = context
    add = {
        'artikel': posts,                 # <- gunakan ini di template
        'data': data_profil,
        'list_kategori': list_kategori,
        'data': data_profil
    }
    src = {**sumber, **add}
    return render(request, 'admin_page.html', src)

@login_required
def edit(request, nm_slug):
    obj, form_cls, kind = resolve_post_by_slug(nm_slug)

    # opsional: batasi agar hanya author atau staff yang bisa edit
    if obj.author != request.user and not request.user.is_staff:
        raise Http404()

    data_profil, _ = Profile.objects.get_or_create(user=request.user)

    if request.method == "POST":
        form = form_cls(request.POST, request.FILES, instance=obj)
        if form.is_valid():
            saved = form.save(commit=False)
            saved.author = obj.author  # jaga author
            saved.save()
            # kalau ada TaggableManager
            if hasattr(form, "save_m2m"):
                form.save_m2m()
            messages.success(request, "Artikel berhasil diupdate.")
            return redirect("core:halaman-admin")
        messages.error(request, "Form tidak valid. Periksa kembali input.")
    else:
        initial = {}
        if hasattr(obj, "tags"):  # kalau model ini pakai taggit
            initial["tags"] = ", ".join(obj.tags.values_list("name", flat=True))
        form = form_cls(instance=obj, initial=initial)
    sumber = context
    add = {
        "form": form,
        "data": data_profil,
        "judul": "Edit Artikel",
        "kind": kind,   # kalau mau tampilkan badge "Advertorial" dll.
    }
    src = {**sumber, **add}
    return render(request, "edit.html", src)

@login_required
def hapus(request, nm_slug):
    obj, _form_cls, _kind = resolve_post_by_slug(nm_slug)

    if obj.author != request.user and not request.user.is_staff:
        raise Http404()

    # hapus file Cloudinary jika ada
    if getattr(obj, "thumbnail", None) and hasattr(obj.thumbnail, "public_id"):
        destroy(obj.thumbnail.public_id)

    obj.delete()
    messages.info(request, "Data berhasil dihapus")
    return redirect("core:halaman-admin")

@login_required
def ads_bayar(request, nm_slug):
    art = get_object_or_404(
    PaidArticle,
    slug_art=nm_slug,
    type='Ads',
    status='pending',
    )
    def ribuan(n: int) -> str:
        return f"{int(n):,}".replace(",", ".")
    bayar = ribuan(13000 * art.duration)

    # batasi akses: hanya author atau staff yang boleh memproses
    if not (request.user == art.author or request.user.is_staff):
        messages.error(request, 'Kamu tidak berhak mengakses pembayaran iklan ini.')
        return redirect('core:halaman-daftar-artikel')  # atau halaman lain

    if request.method == 'POST':
        # fake payment success
        art.status = 'posted'
        art.save(update_fields=['status'])
        messages.success(request, 'Pembayaran berhasil. Iklan telah dipublikasikan.')
        return redirect('core:halaman-admin')

    return render(request, 'payment.html', {'artikel': art, 'harga':bayar})