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
    

# =========================
# CAFETERIA
# =========================

class Produto(models.Model):

    CATEGORIA_CHOICES = [
        ('cafe', 'Cafés'),
        ('gelada', 'Bebidas Geladas'),
        ('comida', 'Comidas'),
        ('sobremesa', 'Sobremesas'),
    ]

    nome = models.CharField(max_length=100)
    descricao = models.CharField(max_length=200)

    preco = models.DecimalField(
        max_digits=6,
        decimal_places=2
    )

    categoria = models.CharField(
        max_length=20,
        choices=CATEGORIA_CHOICES
    )

    disponivel = models.BooleanField(default=True)

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = 'Produto'
        verbose_name_plural = 'Produtos'


class Pedido(models.Model):

    STATUS_CHOICES = [
        ('pendente', 'Pendente'),
        ('confirmado', 'Confirmado'),
        ('cancelado', 'Cancelado'),
    ]

    usuario = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    data_pedido = models.DateTimeField(auto_now_add=True)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pendente'
    )

    total = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        default=0
    )

    def __str__(self):
        return f"Pedido #{self.id} — {self.usuario.username}"

    class Meta:
        verbose_name = 'Pedido'
        verbose_name_plural = 'Pedidos'


class ItemPedido(models.Model):

    pedido = models.ForeignKey(
        Pedido,
        on_delete=models.CASCADE,
        related_name='itens'
    )

    produto = models.ForeignKey(
        Produto,
        on_delete=models.CASCADE
    )

    quantidade = models.IntegerField(default=1)

    preco_unitario = models.DecimalField(
        max_digits=6,
        decimal_places=2
    )

    def subtotal(self):
        return self.quantidade * self.preco_unitario

    def __str__(self):
        return f"{self.quantidade}x {self.produto.nome}"
