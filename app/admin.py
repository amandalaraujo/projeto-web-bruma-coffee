from django.contrib import admin
from app.models import Genero, Tipo, Livro, Reserva, Perfil

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


from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

# Inline para mostrar o perfil dentro da página do usuário no admin
class PerfilInline(admin.StackedInline):
    model = Perfil
    can_delete = False
    verbose_name_plural = 'Perfil'

# Extendendo o UserAdmin padrão
class UserAdmin(BaseUserAdmin):
    inlines = (PerfilInline,)

# Re-registrar User
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
