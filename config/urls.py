from django.contrib import admin
from django.urls import path

from django.conf import settings
from django.conf.urls.static import static

from app import views


urlpatterns = [

    path('', views.index, name='index'),

    path('login/', views.login, name='login'),
    path('registro/', views.registro, name='registro'),
    path('logout/', views.logout, name='logout'),

    # =========================
    # LIVRARIA
    # =========================

    path('livraria/', views.livraria, name='livraria'),

    path(
        'livro/<int:livro_id>/',
        views.livro_detalhes,
        name='livro_detalhes'
    ),

    path(
        'livro/<int:livro_id>/reservar/',
        views.reservar_livro,
        name='reservar_livro'
    ),

    path('reservas/', views.reservas, name='reservas'),

    path(
        'cancelar/<int:reserva_id>/',
        views.cancelar_reserva,
        name='cancelar_reserva'
    ),

    # =========================
    # CAFETERIA
    # =========================

    path('cafeteria/', views.cafeteria, name='cafeteria'),

    path(
        'carrinho/',
        views.carrinho,
        name='carrinho'
    ),

    path(
        'carrinho/adicionar/<int:produto_id>/',
        views.adicionar_carrinho,
        name='adicionar_carrinho'
    ),

    path(
        'carrinho/remover/<int:produto_id>/',
        views.remover_carrinho,
        name='remover_carrinho'
    ),

    path(
        'carrinho/finalizar/',
        views.finalizar_pedido,
        name='finalizar_pedido'
    ),

    path(
        'meus-pedidos/',
        views.meus_pedidos,
        name='meus_pedidos'
    ),

    path('sobre/', views.sobre, name='sobre'),

    path('admin/', admin.site.urls),

] + static(
    settings.MEDIA_URL,
    document_root=settings.MEDIA_ROOT
) + static(
    settings.STATIC_URL,
    document_root=settings.STATIC_ROOT
)