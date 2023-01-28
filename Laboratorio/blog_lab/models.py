from django.db import models

# Create your models here.
from unittest.util import _MAX_LENGTH
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Publicacion(models.Model):
    titulo=models.CharField(max_length=100)
    subtitulo=models.CharField(max_length=100)
    texto=models.TextField(max_length=1000000000)
    autor=models.ForeignKey(User, on_delete=models.CASCADE)
    imagen=models.ImageField(upload_to='photos',null=True, blank=True)
    fecha= models.DateTimeField(default=timezone.now)
    def __str__(self) -> str:
        return self.titulo


class Avatar(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    imagen = models.ImageField(upload_to='avatares',null=True, blank=True)
    def __str__(self):
        return f"Imagen de: {self.user}"

class Comentario(models.Model):
    comentario=models.CharField(max_length=300)
    disertante=models.ForeignKey(User, on_delete=models.CASCADE)
    fecha= models.DateTimeField(default=timezone.now)
    def __str__(self) -> str:
        return self.comentario