from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import *
from user.models import *
from cloudinary.uploader import destroy
from django.db.models import Q
from datetime import date



context = {
    'navbar': 'snippets/navbar.html',
    'simple_navbar': 'snippets/simple_navbar.html',
    'footer': 'snippets/footer.html',
    'judul' : 'Homepage',
    'desc' : 'testing reset belajar',
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
}


# Create your views here.
def main_page(request):
    
    if request.user.is_authenticated:
        data_profil, _ = Profile.objects.get_or_create(user=request.user)
    else:
        data_profil = None
    artikel = Article.objects.all()
    tambahan = {
        'data':data_profil,
        'news':artikel,
    }
    sumber = context
    src ={**tambahan, **sumber}

    return render(request, 'home.html', src)

def admin_article_form(request):
    form = FormTambahArtikel(request.POST or None, request.FILES or None)
    salah = None

    sumber = context
    tambahan = {
        'form': form,
        'salah': salah,
    }
    src = {**sumber, **tambahan}

    if request.method == 'POST':
        if form.is_valid():
            article = form.save(commit=False)   # simpan bentar
            article.author = request.user       # isi author dng user login
            article.save()                      # rill simpan ke DB
            messages.info(request, 'Data berhasil ditambahkan')
            return redirect('core:halaman-admin')
        else:
            salah = form.errors
    return render(request, 'admin_form.html', src)

def admin_article_list(request):
    artikel = Article.objects.filter(author = request.user)
    data_profil, _ = Profile.objects.get_or_create(user=request.user)
    artikel = (Article.objects.select_related('kategori', 'author').filter(author = request.user))

    kategori = request.GET.get('kategori', '')
    cari = request.GET.get('cari', '')
    hari = request.GET.get('hari', '')
    sort = request.GET.get('sort', 'update_desc')

    if cari :
        artikel = artikel.filter(Q(judul__icontains=cari)| Q(author__username__icontains=cari))
    
    if kategori:
        artikel = artikel.filter(kategori__judul=kategori)

    if hari:
        try:
            d = date.fromisoformat(hari)
            artikel = artikel.filter(pubdate__date = d)
        except ValueError:
            pass

    if sort == 'update_asc':
        artikel = artikel.order_by('update')
    elif sort == 'viewer_desc':
        artikel = artikel.order_by('-view_count')
    elif sort == 'viewer_asc':
        artikel = artikel.order_by('view_count')
    else:  # default
        artikel = artikel.order_by('-update')

    list_kategori = (Kategori.objects
                    .order_by('judul')
                    .values_list('judul', flat=True)
                    .distinct())

    sumber = context
    tambahan = {
        'artikel' : artikel,
        'data': data_profil,
        'list_kategori': list_kategori,
    }

    src = {**sumber, **tambahan}
    return render(request, 'admin_page.html', src)

def edit(request, nm_slug):
    obj_artikel = get_object_or_404(Article, slug_art = nm_slug)

    if request.method == 'POST':
        form = FormTambahArtikel(request.POST or None, request.FILES or None, instance=obj_artikel)
        if form.is_valid():
            form.save()

            return redirect('core:halaman-admin')
    else:
        form = FormTambahArtikel(instance=obj_artikel)

    salah = None
    sumber = context
    tambahan = {
        'form' : form,
        'salah' : salah,
    }

    # block text-sm font-semibold text-gray-700 mb-2
    # add_class:"2xl:w-full xl:w-full border border-gray-300 rounded-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-200 auto-resize

    src = {**sumber, **tambahan}
    return render(request, 'edit.html', src)

def hapus(request, nm_slug):
    article = get_object_or_404(Article, slug_art=nm_slug)
    
    if article.thumbnail and hasattr(article.thumbnail, "public_id"):
        destroy(article.thumbnail.public_id)

    article.delete()
    messages.info(request, 'Data berhasil dihapus')
    return redirect('core:halaman-admin')

def detail_artikel(request, nm_slug):
    article = get_object_or_404(Article, slug_art=nm_slug)
    sumber = context
    tambahan = {
        'artikel': article
    }

    if request.user.is_authenticated:
        session_key = f"viewed_{request.user.id}_{article.slug_art}"
    else:
        session_key = f"viewed_guest_{article.slug_art}"

    if not request.session.get(session_key, False):
        article.view_count += 1
        article.save(update_fields=['view_count'])
        request.session[session_key] = True

    src = {**sumber, **tambahan}

    return render(request, 'detail_artikel.html', src)

