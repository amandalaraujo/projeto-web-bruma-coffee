from django.db import models
from django.contrib.auth.models import User

from .catalogo import Genero, Tipo


class Livro(models.Model):
    codigo = models.IntegerField(primary_key=True)
    titulo = models.CharField(max_length=200)
    autor = models.CharField(max_length=200)
    sinopse = models.TextField()
    genero = models.ForeignKey(
        Genero,
        on_delete=models.CASCADE,
        related_name='livros',
    )
    tipo = models.ForeignKey(
        Tipo,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    reservado = models.BooleanField(default=False)
    capa_url = models.URLField(blank=True, null=True)
    favoritado_por = models.ManyToManyField(
        User,
        related_name='livros_favoritos',
        blank=True,
    )

    class Meta:
        verbose_name = 'Livro'
        verbose_name_plural = 'Livros'
        ordering = ['titulo']

    def __str__(self):
        return self.titulo
