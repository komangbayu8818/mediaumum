from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from cloudinary.models import CloudinaryField
# Create your models here.



class Profile(models.Model):
    GENDER_CHOICES = [('-', '-'), ('M','Pria'), ('F','Wanita')]
    MARITAL_CHOICES = [('-', '-'), ('single','Tidak kawin'), ('married','Kawin'), ('private','Private')]
    EDU_CHOICES = [
    ('-', '-'),
    ('tidak_sekolah', 'Tidak/Belum Sekolah'),
    ('sd', 'SD / Sederajat'),
    ('smp', 'SMP / Sederajat'),
    ('sma', 'SMA / Sederajat'),
    ('diploma1', 'Diploma 1 (D1)'),
    ('diploma2', 'Diploma 2 (D2)'),
    ('diploma3', 'Diploma 3 (D3)'),
    ('sarjana', 'Sarjana (S1)'),
    ('magister', 'Magister (S2)'),
    ('doktor', 'Doktor (S3)')
    ]

    JOB_CHOICES = [
    ('-', '-'),
    ('pelajar', 'Pelajar'),
    ('mahasiswa', 'Mahasiswa'),
    ('pns', 'Pegawai Negeri Sipil'),
    ('karyawan_swasta', 'Karyawan Swasta'),
    ('wiraswasta', 'Wiraswasta'),
    ('dokter', 'Dokter'),
    ('perawat', 'Perawat'),
    ('guru', 'Guru'),
    ('dosen', 'Dosen'),
    ('petani', 'Petani'),
    ('nelayan', 'Nelayan'),
    ('buruh', 'Buruh'),
    ('driver', 'Driver / Sopir'),
    ('programmer', 'Programmer'),
    ('desainer', 'Desainer'),
    ('seniman', 'Seniman'),
    ('pengacara', 'Pengacara'),
    ('notaris', 'Notaris'),
    ('tentara', 'Tentara'),
    ('polisi', 'Polisi'),
    ('lainnya', 'Lainnya'),
    ]

    PROVINCE_CHOICES = [
    ('-', '-'),
    ('aceh', 'Aceh'),
    ('sumut', 'Sumatera Utara'),
    ('sumbar', 'Sumatera Barat'),
    ('riau', 'Riau'),
    ('kep_riau', 'Kepulauan Riau'),
    ('jambi', 'Jambi'),
    ('sumsel', 'Sumatera Selatan'),
    ('babel', 'Kepulauan Bangka Belitung'),
    ('bengkulu', 'Bengkulu'),
    ('lampung', 'Lampung'),
    ('dkijakarta', 'DKI Jakarta'),
    ('jabar', 'Jawa Barat'),
    ('jateng', 'Jawa Tengah'),
    ('yogyakarta', 'DI Yogyakarta'),
    ('jatim', 'Jawa Timur'),
    ('banten', 'Banten'),
    ('bali', 'Bali'),
    ('ntb', 'Nusa Tenggara Barat'),
    ('ntt', 'Nusa Tenggara Timur'),
    ('kalbar', 'Kalimantan Barat'),
    ('kalteng', 'Kalimantan Tengah'),
    ('kalsel', 'Kalimantan Selatan'),
    ('kaltim', 'Kalimantan Timur'),
    ('kalut', 'Kalimantan Utara'),
    ('sulut', 'Sulawesi Utara'),
    ('sulteng', 'Sulawesi Tengah'),
    ('sulsel', 'Sulawesi Selatan'),
    ('sultra', 'Sulawesi Tenggara'),
    ('gorontalo', 'Gorontalo'),
    ('sulbar', 'Sulawesi Barat'),
    ('malut', 'Maluku Utara'),
    ('maluku', 'Maluku'),
    ('papua', 'Papua'),
    ('papua_barat', 'Papua Barat'),
    ('papua_tengah', 'Papua Tengah'),
    ('papua_pegunungan', 'Papua Pegunungan'),
    ('papua_selatan', 'Papua Selatan'),
    ('papua_baratdaya', 'Papua Barat Daya'),
    ]

    foto_profil = CloudinaryField('image', null=True, blank=True)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
    nomor_handphone = models.CharField(max_length=20, blank=True, default='-')
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True, default='-')
    tanggal_lahir = models.DateField(null=True, blank=True)
    status_pernikahan = models.CharField(max_length=10, choices=MARITAL_CHOICES, blank=True, default='-')

    alamat = models.CharField(max_length=255, blank=True, default='-')
    provinsi = models.CharField(max_length=100, choices=PROVINCE_CHOICES, blank=True, default='-')
    kota = models.CharField(max_length=100, blank=True, default='-')
    kode_pos = models.CharField(max_length=10, blank=True, default='-')

    pendidikan_terakhir = models.CharField(max_length=20, choices=EDU_CHOICES, blank=True, default='-')
    pekerjaan = models.CharField(max_length=100, choices=JOB_CHOICES, blank=True, default='-')

    def __str__(self):
        return f'Profile({self.user.username})'
    
    @property
    def username(self):
        return self.user.username

    @property
    def first_name(self):
        return self.user.first_name

    @property
    def last_name(self):
        return self.user.last_name
    





    
