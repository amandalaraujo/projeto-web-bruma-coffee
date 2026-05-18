"""
Views relacionadas ao catálogo de livros: listagem, detalhes e favoritos.
Inclui também as procedures (lógica de negócio) para manipulação de livros.
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse

from app.models import Livro, Genero, Tipo


# ---------------------------------------------------------------------------
# Procedures — lógica de negócio isolada
# ---------------------------------------------------------------------------

def procedure_listar_livros():
    """Retorna todos os livros cadastrados."""
    return Livro.objects.all()


def procedure_adicionar_livro(dados):
    """Cria e persiste um novo livro a partir de um dicionário de dados."""
    genero = get_object_or_404(Genero, pk=dados.get('genero_id'))
    tipo = get_object_or_404(Tipo, pk=dados.get('tipo_id'))
    return Livro.objects.create(
        codigo=dados.get('codigo'),
        titulo=dados.get('titulo'),
        autor=dados.get('autor'),
        sinopse=dados.get('sinopse'),
        genero=genero,
        tipo=tipo,
        capa_url=dados.get('capa_url'),
    )


def procedure_remover_livro(livro_id, is_admin=False):
    """Remove um livro pelo ID. Apenas administradores devem chamar esta função."""
    livro = get_object_or_404(Livro, pk=livro_id)
    livro.delete()


def procedure_atualizar_livro(livro_id, dados):
    """Atualiza os campos de um livro existente."""
    livro = get_object_or_404(Livro, pk=livro_id)
    livro.titulo = dados.get('titulo', livro.titulo)
    livro.autor = dados.get('autor', livro.autor)
    livro.sinopse = dados.get('sinopse', livro.sinopse)
    if 'genero_id' in dados:
        livro.genero = get_object_or_404(Genero, pk=dados.get('genero_id'))
    livro.save()
    return livro


# ---------------------------------------------------------------------------
# Views
# ---------------------------------------------------------------------------

def livraria(request):
    """Lista todos os livros disponíveis na livraria com suporte a busca e filtros."""
    query = request.GET.get('q')
    genero_id = request.GET.get('genero')
    
    livros = Livro.objects.all()
    
    if query:
        livros = livros.filter(titulo__icontains=query) | livros.filter(autor__icontains=query)
        
    if genero_id:
        livros = livros.filter(genero_id=genero_id)
        
    generos = Genero.objects.all()
    
    return render(request, 'livraria.html', {
        'books': livros,
        'generos': generos,
        'query': query,
        'genero_selecionado': int(genero_id) if genero_id else None
    })


def livro_detalhes(request, livro_id):
    """Exibe os detalhes de um livro específico."""
    livro = get_object_or_404(Livro, pk=livro_id)
    is_favorito = False
    if request.user.is_authenticated:
        is_favorito = livro.favoritado_por.filter(id=request.user.id).exists()
    return render(request, 'livro_detalhes.html', {
        'livro': livro,
        'is_favorito': is_favorito,
    })


@login_required
def favoritar_livro(request, livro_id):
    """Adiciona ou remove um livro dos favoritos do usuário autenticado."""
    livro = get_object_or_404(Livro, pk=livro_id)
    if livro.favoritado_por.filter(id=request.user.id).exists():
        livro.favoritado_por.remove(request.user)
        messages.info(request, f'"{livro.titulo}" removido dos favoritos.')
    else:
        livro.favoritado_por.add(request.user)
        messages.success(request, f'"{livro.titulo}" adicionado aos favoritos!')
    return redirect('livro_detalhes', livro_id=livro_id)


def busca_preditiva(request):
    """Retorna uma lista de livros em JSON para o autocomplete da busca."""
    query = request.GET.get('q', '')
    results = []
    
    if len(query) >= 2:
        livros = Livro.objects.filter(titulo__icontains=query) | Livro.objects.filter(autor__icontains=query)
        for livro in livros[:5]:  # Limita a 5 sugestões
            results.append({
                'titulo': livro.titulo,
                'autor': livro.autor,
                'codigo': livro.codigo,
                'capa': livro.capa_url if livro.capa_url else None
            })
            
    return JsonResponse({'results': results})
