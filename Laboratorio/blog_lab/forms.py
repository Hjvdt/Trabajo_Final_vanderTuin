from dataclasses import fields
from socket import fromshare
from django import forms 
from django.contrib.auth.models import User
from django.contrib.auth.forms import  UserCreationForm

from blog_lab.models import *


class UserRegisterForm(UserCreationForm):
    first_name=forms.CharField(label='Nombre')
    last_name=forms.CharField(label='Apellido')
    email = forms.EmailField(label='Email')
    password1= forms.CharField(label='Contraseña', widget=forms.PasswordInput)
    password2= forms.CharField(label='Repetir la contraseña', widget=forms.PasswordInput)

    class Meta:
        model=User
        fields=['username','first_name','last_name','email','password1','password2']
        help_texts = {k:"" for k in fields}

class UserEditForm(UserCreationForm):
    email = forms.EmailField(label='Modificar email',required=False)
    password1= forms.CharField(label='Modificar contraseña', widget=forms.PasswordInput,required=False)
    password2= forms.CharField(label='Repetir contraseña nueva', widget=forms.PasswordInput,required=False)
    first_name=forms.CharField(label='Modificar nombre',required=False)
    last_name=forms.CharField(label='Modificar apellido',required=False)

    class Meta:
        model=User
        fields=['first_name','last_name','email','password1','password2']
        help_texts = {k:"" for k in fields}

class FormPublicacion(forms.Form):
    titulo=forms.CharField(max_length=100,required=False)
    subtitulo=forms.CharField(max_length=100,required=False)
    texto=forms.CharField(max_length=1000000000,required=False)
    imagen=forms.ImageField(required=False)

class AvatarForm(forms.ModelForm):
    #imagen=forms.ImageField(label='Imagen')
    class Meta:
        model = Avatar
        fields = ['imagen']

class FormCom(forms.Form):
    comentario=forms.CharField(label='Comentario',max_length=300)