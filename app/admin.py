from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from app.models import Genero, Tipo, Livro, Reserva, Perfil, Produto, Pedido, ItemPedido

# --- Configurações de Livros e Biblioteca ---

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


# --- Configurações da Cafeteria (Bruma and Coffee) ---

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


# --- Configurações de Usuários e Perfis ---

# Inline para mostrar o perfil dentro da página do usuário no admin
class PerfilInline(admin.StackedInline):
    model = Perfil
    can_delete = False
    verbose_name_plural = 'Perfil'

# Estendendo o UserAdmin padrão para incluir o Perfil de forma integrada
class UserAdmin(BaseUserAdmin):
    inlines = (PerfilInline,)

# Re-registrar o User padrão do Django com a nossa nova configuração
admin.site.unregister(User)
admin.site.register(User, UserAdmin)

@admin.register(Perfil)
class PerfilAdmin(admin.ModelAdmin):
    list_display = ('get_username', 'get_first_name', 'sobrenome', 'telefone')
    search_fields = ('usuario__username', 'usuario__first_name', 'sobrenome')

    def get_username(self, obj):
        return obj.usuario.username
    get_username.short_description = 'Usuário'

    def get_first_name(self, obj):
        return obj.usuario.first_name
    get_first_name.short_description = 'Nome'