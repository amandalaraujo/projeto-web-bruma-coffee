from .auth import login, registro, logout, perfil, pedidos, configuracoes
from .livros import (
    livraria,
    livro_detalhes,
    favoritar_livro,
    busca_preditiva,
    procedure_listar_livros,
    procedure_adicionar_livro,
    procedure_remover_livro,
    procedure_atualizar_livro,
)
from .reservas import reservar_livro, lista_reservas, cancelar_reserva
from .paginas import index, sobre
from .cafeteria import (
    cafeteria,
    adicionar_carrinho,
    remover_carrinho,
    carrinho,
    finalizar_pedido,
    meus_pedidos,
)

__all__ = [
    'login',
    'registro',
    'logout',
    'perfil',
    'pedidos',
    'configuracoes',
    'livraria',
    'livro_detalhes',
    'favoritar_livro',
    'busca_preditiva',
    'procedure_listar_livros',
    'procedure_adicionar_livro',
    'procedure_remover_livro',
    'procedure_atualizar_livro',
    'reservar_livro',
    'lista_reservas',
    'cancelar_reserva',
    'index',
    'sobre',
    'cafeteria',
    'adicionar_carrinho',
    'remover_carrinho',
    'carrinho',
    'finalizar_pedido',
    'meus_pedidos',
]
