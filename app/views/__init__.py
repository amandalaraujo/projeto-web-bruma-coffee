"""
Pacote de views do app.

Organização por categoria:
  - auth.py     → login, registro, logout
  - livros.py   → livraria, livro_detalhes, favoritar_livro
                  + procedures: procedure_listar_livros, procedure_adicionar_livro,
                                procedure_remover_livro, procedure_atualizar_livro
  - reservas.py → reservar_livro, reservas, cancelar_reserva
  - paginas.py  → index, sobre, cafeteria
"""

from .auth import login, registro, logout
from .livros import (
    livraria,
    livro_detalhes,
    favoritar_livro,
    procedure_listar_livros,
    procedure_adicionar_livro,
    procedure_remover_livro,
    procedure_atualizar_livro,
)
from .reservas import reservar_livro, lista_reservas, cancelar_reserva
from .paginas import index, sobre, cafeteria

__all__ = [
    # auth
    'login',
    'registro',
    'logout',
    # livros
    'livraria',
    'livro_detalhes',
    'favoritar_livro',
    'procedure_listar_livros',
    'procedure_adicionar_livro',
    'procedure_remover_livro',
    'procedure_atualizar_livro',
    # reservas
    'reservar_livro',
    'lista_reservas',
    'cancelar_reserva',
    # paginas
    'index',
    'sobre',
    'cafeteria',
]
