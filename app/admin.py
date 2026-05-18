from django.contrib import admin
from .models import Genero, Tipo, Livro, Reserva

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
