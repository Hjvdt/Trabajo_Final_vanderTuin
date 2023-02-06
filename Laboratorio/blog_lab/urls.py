from django.urls import path
from blog_lab.views import *
from django.contrib.auth.views import LogoutView, LoginView
from django.views.generic.edit import DeleteView
from blog_lab import views


urlpatterns = [
    path('login/', login_request, name='login'),
    path('registro/', registro, name='registro'),
    path('logout/', LogoutView.as_view(template_name='blog_lab/inicio.html'), name='logout'),
    path('editarPerfil/', editarPerfil, name='editarPerfil'),
    path('', inicio, name='inicio'),
    path('about/', sobreMi ,name='sobreMi'),
    path('agregar-Avatar/', agregar_Avatar, name='agregar_Avatar'),
    path('comentarios/', comentarios, name='comentarios'),
    path('publicaciones/', publicaciones, name='publicaciones'),
    path('pages/', leer_Publicaciones, name='leerPublicacion' ),
    path('eliminarPublicacion/<publicacion_publicacion>/', views.eliminarPublicacion , name='eliminarPublicacion' ),
    path('editarPublicacion/<publicacion_publicacion>/', views.editarPublicacion , name='editarPublicacion' ),    
]
   