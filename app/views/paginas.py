"""
Views de páginas gerais: página inicial, sobre e cafeteria.
"""

from django.shortcuts import render

from app.models import Livro


def index(request):
    """Exibe a página inicial com os primeiros livros do catálogo."""
    livros = Livro.objects.all()[:5]
    return render(request, 'index.html', {'books': livros})


def sobre(request):
    """Exibe a página institucional 'Sobre'."""
    return render(request, 'sobre.html')


def cafeteria(request):
    """Exibe a página da cafeteria."""
    return render(request, 'cafeteria.html')
