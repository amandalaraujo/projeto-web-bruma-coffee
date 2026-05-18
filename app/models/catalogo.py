from django.db import models


class Genero(models.Model):
    codigo = models.IntegerField(primary_key=True)
    nome = models.CharField(max_length=100)

    class Meta:
        verbose_name = 'Gênero'
        verbose_name_plural = 'Gêneros'
        ordering = ['nome']

    def __str__(self):
        return self.nome


class Tipo(models.Model):
    codigo = models.IntegerField(primary_key=True)
    nome = models.CharField(max_length=100)

    class Meta:
        verbose_name = 'Tipo'
        verbose_name_plural = 'Tipos'
        ordering = ['nome']

    def __str__(self):
        return self.nome
