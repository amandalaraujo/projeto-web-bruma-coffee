from django.db import models
from django.contrib.auth.models import User

from .livro import Livro


class Reserva(models.Model):
    usuario = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reservas_usuario',
    )
    livro = models.ForeignKey(
        Livro,
        on_delete=models.CASCADE,
        related_name='reservas_livro',
    )
    data_emprestimo = models.DateTimeField(auto_now_add=True)
    data_devolucao = models.DateTimeField(null=True, blank=True)
    data_limite = models.DateTimeField()
    taxa = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    cancelado = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Reserva'
        verbose_name_plural = 'Reservas'
        ordering = ['-data_emprestimo']

    def __str__(self):
        return f'{self.usuario.username} — {self.livro.titulo}'
