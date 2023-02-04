from email.mime import image
from operator import le
from pyexpat.errors import messages
from django.core.checks import Error
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.http import HttpResponse
from django.shortcuts import render

from django.template import Context, Template,loader
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User

from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView

from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages

from blog_lab.models import *
from blog_lab.forms import *

# login y registro

def login_request(request):
    if request.method=='POST':
        form=AuthenticationForm(request, data = request.POST)
        if form.is_valid():
            user=form.cleaned_data.get('username')
            password=form.cleaned_data.get('password')
            usuario = authenticate(username=user,password=password)
            if usuario is not None:
                login(request, usuario)
                return render (request, 'blog_lab/inicio.html')
            else:
                return render(request, 'blog_lab/login.html', {'mensaje':f'No se pudo iniciar sesión. Datos incorrectos.','form':form} )
        else:
            return  render(request, 'blog_lab/login.html', {'mensaje':f'Error, formulario erróneo.', 'form':form} )
    form=AuthenticationForm()
    return  render(request, 'blog_lab/login.html', {'form':form} )

def registro(request):
    if request.method=='POST':
        form=UserRegisterForm(request.POST)
        if form.is_valid():
            username=form.cleaned_data.get('username')
            form.save()
            return render (request, 'blog_lab/inicio.html', {'mensaje':'Usuario creado exitosamente!'} )
    else:
        form = UserRegisterForm()
    return  render(request, 'blog_lab/registro.html', {'form':form, 'imagen':traerAvatar(request) } )


# Perfil y Avatar
    
@login_required
def editarPerfil(request):
    usuario = request.user
    if request.method=='POST':
        form=UserEditForm(request.POST)
        if form.is_valid():
            info = form.cleaned_data
            usuario.email = info['email']
            usuario.password1 = info['password1']
            usuario.password2 = info['password2']
            usuario.first_name = info['first_name']
            usuario.last_name = info['last_name']
            usuario.save()
            return render (request, 'blog_lab/inicio.html', {'mensaje':f'Usuario editado'})
    else:
        form=UserEditForm(request.POST)
    return render (request, 'blog_lab/editarUser.html', {'form':form,'usuario':usuario, 'imagen':traerAvatar(request) })

@login_required
def agregar_Avatar(request):
    if request.method == "POST":
        formulario = AvatarForm(request.POST, request.FILES, instance=request.user.avatar) 
        if formulario.is_valid():
            #avatar=Avatar(user=request.user, imagen=formulario.cleaned_data['imagen'])
            avatar=formulario.save()
            avatar.user=request.user
            avatar.save()
            url_exitosa=reverse_lazy('inicio')
            return redirect(url_exitosa)
            
    else:
        formulario=AvatarForm(instance=request.user.avatar)
    return render(
        request=request, 
        template_name='blog_lab/formulario_Avatar.html',
        context={'formulario':formulario,'usuario':request.user} )


@login_required
def traerAvatar(request):
    lista=Avatar.objects.filter(user=request.user)
    if len(lista)!=0:
        imagen=lista[0].imagen.url
    else:
        imagen=''
    return imagen


def inicio (request):
    comentarios = Comentario.objects.all()
    return render (request,"blog_lab/inicio.html",{'imagen':traerAvatar(request),'comentarios': comentarios})

def sobreMi (request):
    return render (request, "blog_lab/sobreMi.html",{'imagen':traerAvatar(request)} )

# Publicacion del Blog
@login_required
def publicaciones (request):
    if request.method == "POST":
        nuevaPublicacion=FormPublicacion(request.POST,request.FILES)
        print(nuevaPublicacion.is_valid())
        imagen=request.FILES['imagen']
        if nuevaPublicacion.is_valid():
            informacion=nuevaPublicacion.cleaned_data
            user=request.user
            titulo=informacion.get("titulo")
            subtitulo=informacion.get("subtitulo")
            texto=informacion.get("texto")
            imagen=informacion.get("imagen")
            publicacion=Publicacion(titulo=titulo,subtitulo=subtitulo,autor=user,
            texto=texto,imagen=imagen)
            publicacion.save()
            return render(request, "blog_lab/inicio.html",{'usuario':request.user} )
        else:
            print(nuevaPublicacion.errors)
            return render(request, "blog_lab/inicio.html")
    else:
        nuevaPublicacion=FormPublicacion()
        return render (request, "blog_lab/publicaciones.html",{'form':nuevaPublicacion, 'usuario':request.user ,'imagen':traerAvatar(request) } )

def leer_Publicaciones (request):
    publicaciones = Publicacion.objects.all()
    texto='No hay publicaciones para ver.'
    if publicaciones:
        return render (request, 'blog_lab/leerPublicacion.html', {'publicaciones': publicaciones,'imagen':traerAvatar(request)})
    return render (request, 'blog_lab/leerPublicacion.html', {'texto':texto ,'imagen':traerAvatar(request)})


@login_required
def editarPublicacion (request, publicacion_id):
    publicacion = Publicacion.objects.get(titulo=publicacion_id)
     
    if request.method =='POST':
        form=FormPublicacion(request.POST,request.FILES)
        if form.is_valid():
            info=form.cleaned_data
            publicacion.titulo = info['titulo']
            publicacion.subtitulo = info['subtitulo']
            publicacion.texto = info['texto']
            if info['imagen']:
                publicacion.imagen = info['imagen']
            publicacion.save()
            publicaciones=Publicacion.objects.all()
            return render (request,"blog_lab/leerPublicacion.html",{'publicaciones':publicaciones})
    else: 
        form=FormPublicacion(initial={'titulo': publicacion.titulo,
        'subtitulo':publicacion.subtitulo,'texto':publicacion.texto,'imagen':publicacion.imagen})  
    return render(request, "blog_lab/editarPublicacion.html",
    {'form':form,'publicacion_id':publicacion_id})

@login_required
def eliminarPublicacion (request, publicacion_publicacion):
    publicacion = Publicacion.objects.get(titulo=publicacion_publicacion)
    publicacion.delete()

    publicaciones = Publicacion.objects.all()
    context = {'publicaciones': publicaciones}

    return render( request, 'blog_lab/leerPublicacion.html', context )



# Comentarios

@login_required
def comentarios(request):
    if request.method=='POST':
        formulario=FormCom(request.POST)
        if formulario.is_valid():
            info=formulario.cleaned_data
            comentario=info.get("comentario")
            user=request.user
            ncomentario=Comentario(comentario=comentario, disertante=user)
            ncomentario.save()
            return render (request, 'blog_lab/comentarios.html',{'usuario':request.user})
    else:
        formulario=FormCom()
    return  render(request, 'blog_lab/comentarios.html', {'formulario':formulario, 'imagen':traerAvatar(request) } )


def leerComentarios (request):
    comentarios = Comentario.objects.all()
    texto='No hay comentarios aún.'
    if comentarios:
        return render (request, 'blog_lab/inicio.html', {'comentarios': comentarios})
    return render (request, 'blog_lab/inicio.html', {'texto':texto ,'imagen':traerAvatar(request)})
