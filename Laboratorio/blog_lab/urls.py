from django.urls import path
from blog_lab.views import *
from django.contrib.auth.views import LogoutView, LoginView

urlpatterns = [
    path('login/', login_request, name='login'),
    path('registro/', registro, name='registro'),
    path('logout/', LogoutView.as_view(template_name='blog_lab/inicio.html'), name='logout'),
    path('editarPerfil/', editarPerfil, name='editarPerfil'),
    path('', inicio, name='inicio'),
    path('sobreMi/', sobreMi ,name='sobreMi'),
    path('agregar-Avatar/', agregar_Avatar, name='agregar_Avatar'),
    path('comentarios/', comentarios, name='comentarios'),
    path('publicaciones/', publicaciones, name='publicaciones'),
    path('leerPublicaciones/', leerPublicaciones, name='leerPublicacion' ),
    path('eliminarPublicacion/<publicacion_publicacion>/', eliminarPublicacion , name='eliminarPublicacion' ),
    path('editarPublicacion/<publicacion_publicacion>/', editarPublicacion , name='editarPublicacion' ),    
]


   # path('login/', login_view, name="login"),
   # path('logout/', CustomLogoutView.as_view(), name="logout"),
    # URLS de Perfil
   # path('editar-perfil/', ProfileUpdateView.as_view(), name="editar_perfil"),
   # path('agregar-avatar/', agregar_avatar, name="agregar_avatar"),