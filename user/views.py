from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import *
from cloudinary.uploader import destroy

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
def login_umum(request):
    sumber = context
    user=request.user

    if request.method == 'GET':
        if user.is_authenticated:
            return redirect('core:home')


    if request.method == 'POST':
        username_inp = request.POST['username']
        password_inp = request.POST['password']

        user = authenticate(request, username=username_inp, password=password_inp)

        if user is not None:
            login(request, user)
            return redirect('core:home')
        else:

            messages.error(request, 'Login Gagal Periksa Penulisan Username / Password')
            return redirect('user:login')
    return render(request, 'login.html', sumber)

def register_user(request):

    
    user=request.user
    form = RegisterUserForm(request.POST or None)
    tambahan = {
        'form' : form
    }
    if form.is_valid():
        form.save()
        return redirect('user:login')
    
    if request.method == 'GET':
        if user.is_authenticated:
            return redirect('core:home')
    
    return render(request, 'register.html', tambahan)


def ubah_password(request):
    user = User.objects.get(username=request.user)
    form = UserPasswordChangeForm(request.user, request.POST)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('user:halaman-profil')
        else:
            return redirect('user:halaman-ubah-password')
    else:
        form = UserPasswordChangeForm(request.user)

    sumber = context
    tambahan ={ 'form': form}
    src ={**sumber, **tambahan}
    
    

    return render(request, 'ubah_password.html', src)


@login_required(login_url='/')
def logout_user(request):
    sumber = context
    if request.method == 'POST':
        if request.POST['logout'] == 'logout':
            logout(request)
            return redirect('core:home')
    return render(request, 'logout.html', sumber)

@login_required(login_url='/')
def halaman_profil(request):
    user = request.user
    full_name = user.get_full_name()
    data_profil, _ = Profile.objects.get_or_create(user=user)
    is_admin = user.groups.filter(name='Admin').exists
    sumber = context
    tambahan = {
        'nama_lengkap':full_name,
        'user':user,
        'data':data_profil,
        'admin': is_admin,
    }
    src = {**sumber, **tambahan}
    
    return render(request, 'profil.html', src)

@login_required
def edit_profil(request):
    profile, _ = Profile.objects.get_or_create(user=request.user)
    data_profil, _ = Profile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        user_form = UserRegistDataForm(request.POST, instance=request.user)
        profile_form = UserProfileEditForm(request.POST, instance=profile)
        picture_form = ProfilePicture(request.POST, request.FILES, instance=profile)

        if user_form.is_valid() and profile_form.is_valid() and picture_form.is_valid():
            user_form.save()
            profile_form.save()
            if 'foto_profil-clear' in request.POST:
            # hapus foto lama
                if profile.foto_profil:
                    destroy(profile.foto_profil.public_id)  # hapus file dari storage kalau mau
                    profile.foto_profil = None
                    profile.save(update_fields=['foto_profil'])

                    return redirect('user:halaman-profil')
                else:
                    # kalau tidak dicentang, simpan perubahan dari picture_form
                    picture_form.save()
                    return redirect('user:halaman-profil')

            return redirect('user:halaman-profil')
        else:
            messages.error(request, "Cek kembali input kamu.")
    else:
        user_form = UserRegistDataForm(instance=request.user)
        profile_form = UserProfileEditForm(instance=profile)
        picture_form = ProfilePicture(instance=profile)

    sumber = context
    tambahan = {
        'form_nama': user_form,          # ← kirim INSTANCE
        'form_profile': profile_form,    # ← kirim INSTANCE
        'form_foto_profil':picture_form,
        'data':data_profil,
    }
    src = {**sumber, **tambahan}
    return render(request, 'edit_profil.html', src)