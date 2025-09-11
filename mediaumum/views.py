from django.shortcuts import render

# Create your views here.
def main_page(request):
    context = {
        'navbar': 'snippets/navbar.html',
        'footer': 'snippets/footer.html',
        'judul' : 'Homepage',
        'desc' : 'testing reset belajar',
        'logo' : 'images/mediaumum.png',
        'burger' : 'images/hamburger.png',
        'home' : 'images/home_icon.webp',
        'moon' : 'images/moon_icon.webp',
        'user' : 'images/user.webp',
        'arrow' : 'images/down_arrow.webp',
        'arrow_hover' : 'images/down_arrow_hover.webp',
        'user_hover' : 'images/user_hover.webp',
        'images' : 'images/berita.webp',
        'artikel1': 'images/artikel2.webp',
        'artikel2': 'images/artikel3.webp',
        'iklan1' : 'images/iklan.jpg',
        'iklan2' : 'images/iklan2.webp',
        'tiktok': 'images/tiktok.webp',
        'instagram': 'images/instagram.webp',
        'facebook': 'images/facebook.webp',
    }

    return render(request, 'index.html', context)