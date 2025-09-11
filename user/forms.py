from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth.models import User
from django import forms
from .models import *
from django.forms import FileInput

class RegisterUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']

class UserPasswordChangeForm(PasswordChangeForm):
    class Meta:
        model = User
        fields = ['old_password', 'new_password1', 'new_password2']

class UserRegistDataForm(forms.ModelForm): #Data dari registrasi
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email']

class ProfilePicture(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['foto_profil']
        widgets = {
            'foto_profil': FileInput(attrs={
                'accept': 'image/*',
                'class': 'hidden',
                'id': 'id_foto_profil',
            })
        }


class UserProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile 
        fields = ('__all__')
        exclude = ['user', 'foto_profil']

