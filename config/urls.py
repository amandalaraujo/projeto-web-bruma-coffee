from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from app import views

urlpatterns = [
    # Páginas gerais
    path('', views.index, name='index'),
    path('sobre/', views.sobre, name='sobre'),
    path('cafeteria/', views.cafeteria, name='cafeteria'),

    # Autenticação
    path('login/', views.login, name='login'),
    path('registro/', views.registro, name='registro'),
    path('logout/', views.logout, name='logout'),

    # Catálogo de livros e Favoritos
    path('livraria/', views.livraria, name='livraria'),
    path('livro/<int:livro_id>/', views.livro_detalhes, name='livro_detalhes'),
    path('livro/<int:livro_id>/favoritar/', views.favoritar_livro, name='favoritar_livro'),

    # Reservas de Livros
    path('livro/<int:livro_id>/reservar/', views.reservar_livro, name='reservar_livro'),
    path('reservas/', views.lista_reservas, name='reservas'),
    path('cancelar/<int:reserva_id>/', views.cancelar_reserva, name='cancelar_reserva'),

    # Perfil, Conta e Menu Suspenso
    path('perfil/', views.perfil, name='perfil'),
    path('pedidos/', views.pedidos, name='pedidos'),
    path('configuracoes/', views.configuracoes, name='configuracoes'),

    # Cafeteria
    path('carrinho/', views.carrinho, name='carrinho'),
    path('carrinho/adicionar/<int:produto_id>/', views.adicionar_carrinho, name='adicionar_carrinho'),
    path('carrinho/remover/<int:produto_id>/', views.remover_carrinho, name='remover_carrinho'),
    path('carrinho/finalizar/', views.finalizar_pedido, name='finalizar_pedido'),
    path('meus-pedidos/', views.meus_pedidos, name='meus_pedidos'),

    # API de Busca Preditiva
    path('api/busca-preditiva/', views.busca_preditiva, name='busca_preditiva'),

    # Admin do Django
    path('admin/', admin.site.urls),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
