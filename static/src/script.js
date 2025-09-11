document.addEventListener('click', function (e) {
    const toggleBtn = e.target.closest('[data-toggle]');

    // Klik tombol -> toggle dropdown ini
    if (toggleBtn) {
        const dd = toggleBtn.closest('[data-dropdown]');
        const menu = dd.querySelector('[data-menu]');
        const isOpen = dd.classList.toggle('open');

        // buka/tutup animasi menu
        if (isOpen) {
        menu.classList.remove('opacity-0', 'scale-y-0', 'pointer-events-none');
        // tutup dropdown lain
        document.querySelectorAll('[data-dropdown].open').forEach(function (other) {
            if (other !== dd) {
            other.classList.remove('open');
            other.querySelector('[data-menu]')
                .classList.add('opacity-0', 'scale-y-0', 'pointer-events-none');
            }
        });
        } else {
        menu.classList.add('opacity-0', 'scale-y-0', 'pointer-events-none');
        }
        return; // stop di sini; jangan jalankan handler "klik di luar"
    }

    // Klik di luar -> tutup semua
    document.querySelectorAll('[data-dropdown].open').forEach(function (dd) {
        if (!dd.contains(e.target)) {
        dd.classList.remove('open');
        dd.querySelector('[data-menu]')
            .classList.add('opacity-0', 'scale-y-0', 'pointer-events-none');
        }
    });
    });

    // ESC -> tutup semua
    document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape') {
        document.querySelectorAll('[data-dropdown].open').forEach(function (dd) {
        dd.classList.remove('open');
        dd.querySelector('[data-menu]')
            .classList.add('opacity-0', 'scale-y-0', 'pointer-events-none');
        });
    }
});

// Tutup menu kalau klik di luar menu
document.addEventListener('click', function (event) {
    const allMenus = document.querySelectorAll('details[data-menu]');

    allMenus.forEach(function (menu) {
        const isOpen = menu.hasAttribute('open');
        const clickedInside = menu.contains(event.target);

        if (isOpen && !clickedInside) {
        menu.removeAttribute('open'); // tutup menu
        }
    });
});

// Tutup menu lain saat 1 menu dibuka
document.querySelectorAll('details[data-menu]').forEach(function (menu) {
    menu.addEventListener('toggle', function () {
        if (menu.open) {
        const otherMenus = document.querySelectorAll('details[data-menu]');
        otherMenus.forEach(function (other) {
            if (other !== menu) {
            other.removeAttribute('open');
            }
        });
        }
    });
});

    // Tutup semua menu kalau tekan ESC
    document.addEventListener('keydown', function (event) {
    if (event.key === 'Escape') {
        const openMenus = document.querySelectorAll('details[data-menu][open]');
        openMenus.forEach(function (menu) {
        menu.removeAttribute('open');
        });
    }
});