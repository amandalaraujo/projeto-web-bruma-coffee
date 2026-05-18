from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

# Importa cada módulo de views separadamente para deixar clara a origem de cada rota
from app.views import auth, livros, paginas
import app.views.reservas as views_reservas

urlpatterns = [
    # Páginas gerais
    path('', paginas.index, name='index'),
    path('sobre/', paginas.sobre, name='sobre'),
    path('cafeteria/', paginas.cafeteria, name='cafeteria'),

    # Autenticação
    path('login/', auth.login, name='login'),
    path('registro/', auth.registro, name='registro'),
    path('logout/', auth.logout, name='logout'),

    # Catálogo de livros
    path('livraria/', livros.livraria, name='livraria'),
    path('livro/<int:livro_id>/', livros.livro_detalhes, name='livro_detalhes'),
    path('livro/<int:livro_id>/favoritar/', livros.favoritar_livro, name='favoritar_livro'),

    # Reservas
    path('livro/<int:livro_id>/reservar/', views_reservas.reservar_livro, name='reservar_livro'),
    path('reservas/', views_reservas.lista_reservas, name='reservas'),
    path('cancelar/<int:reserva_id>/', views_reservas.cancelar_reserva, name='cancelar_reserva'),

    # Perfil e Conta
    path('perfil/', auth.perfil, name='perfil'),
    path('pedidos/', auth.pedidos, name='pedidos'),
    path('configuracoes/', auth.configuracoes, name='configuracoes'),

    # API de Busca
    path('api/busca-preditiva/', livros.busca_preditiva, name='busca_preditiva'),

    # Admin do Django
    path('admin/', admin.site.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) \
  + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
