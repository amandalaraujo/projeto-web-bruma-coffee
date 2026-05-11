from django.contrib import admin
from .models import Reserva, Produto, Pedido, ItemPedido


@admin.register(Reserva)
class ReservaAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'autor', 'usuario', 'data_reserva', 'status')
    list_filter = ('status',)
    search_fields = ('titulo', 'autor', 'usuario__username')


@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'categoria', 'preco', 'disponivel')
    list_filter = ('categoria', 'disponivel')
    search_fields = ('nome',)


class ItemPedidoInline(admin.TabularInline):
    model = ItemPedido
    extra = 0


@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ('id', 'usuario', 'data_pedido', 'status', 'total')
    list_filter = ('status',)
    inlines = [ItemPedidoInline]