# models.py
from django.db import models
from django.contrib.auth.models import User

class Reserva(models.Model):
    STATUS_CHOICES = [
        ('reservado', 'Reservado'),
        ('devolvido', 'Devolvido'),
        ('cancelado', 'Cancelado'),
    ]

    # quem reservou
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    
    # dados do livro que vêm da NYT API
    titulo = models.CharField(max_length=200)
    autor = models.CharField(max_length=200)
    capa_url = models.URLField(blank=True)
    
    # controle da reserva
    data_reserva = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='reservado'
    )

    def __str__(self):
        return f"{self.usuario.username} → {self.titulo}"

    class Meta:
        verbose_name = 'Reserva'
        verbose_name_plural = 'Reservas'