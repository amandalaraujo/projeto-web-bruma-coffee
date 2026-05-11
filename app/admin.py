# admin.py
from django.contrib import admin
from .models import Reserva

@admin.register(Reserva)
class ReservaAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'autor', 'usuario', 'data_reserva', 'status')
    list_filter = ('status',)
    search_fields = ('titulo', 'autor', 'usuario__username')