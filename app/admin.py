from django.contrib import admin
from .models import Genero, Tipo, Livro, Reserva, Produto, Pedido, ItemPedido

@admin.register(Genero)
class GeneroAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'nome')

@admin.register(Tipo)
class TipoAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'nome')

@admin.register(Livro)
class LivroAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'titulo', 'autor', 'genero', 'reservado')
    list_filter = ('genero', 'reservado')
    search_fields = ('titulo', 'autor')

@admin.register(Reserva)
class ReservaAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'livro', 'data_emprestimo', 'data_limite', 'cancelado')
    list_filter = ('cancelado', 'data_emprestimo')

@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    list_display = (
        'nome',
        'categoria',
        'preco',
        'disponivel'
    )

    list_filter = (
        'categoria',
        'disponivel'
    )

    search_fields = ('nome',)


class ItemPedidoInline(admin.TabularInline):
    model = ItemPedido
    extra = 0


@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'usuario',
        'data_pedido',
        'status',
        'total'
    )

    list_filter = ('status',)

    inlines = [ItemPedidoInline]
