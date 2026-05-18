from django.db import models
from django.contrib.auth.models import User

class Genero(models.Model):
    codigo = models.IntegerField(primary_key=True)
    nome = models.CharField(max_length=100)

    def __str__(self):
        return self.nome

class Tipo(models.Model):
    codigo = models.IntegerField(primary_key=True)
    nome = models.CharField(max_length=100)

    def __str__(self):
        return self.nome

class Livro(models.Model):
    codigo = models.IntegerField(primary_key=True)
    titulo = models.CharField(max_length=200)
    autor = models.CharField(max_length=200)
    sinopse = models.TextField()
    genero = models.ForeignKey(Genero, on_delete=models.CASCADE, related_name='livros')
    tipo = models.ForeignKey(Tipo, on_delete=models.SET_NULL, null=True, blank=True)
    reservado = models.BooleanField(default=False)
    capa_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.titulo

class Reserva(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reservas_usuario')
    livro = models.ForeignKey(Livro, on_delete=models.CASCADE, related_name='reservas_livro')
    data_emprestimo = models.DateTimeField(auto_now_add=True)
    data_devolucao = models.DateTimeField(null=True, blank=True)
    data_limite = models.DateTimeField()
    taxa = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    cancelado = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.usuario.username} - {self.livro.titulo}"
