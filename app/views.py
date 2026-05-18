from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Livro, Genero, Reserva, Tipo
from django.utils import timezone
from datetime import timedelta
from decimal import Decimal

from .models import (
    Livro,
    Genero,
    Reserva,
    Tipo,
    Produto,
    Pedido,
    ItemPedido
)

# --- Procedures (Lógica de Negócio) ---

def procedure_listar_livros():
    return Livro.objects.all()

def procedure_adicionar_livro(dados):
    genero = get_object_or_404(Genero, pk=dados.get('genero_id'))
    tipo = get_object_or_404(Tipo, pk=dados.get('tipo_id'))
    return Livro.objects.create(
        codigo=dados.get('codigo'),
        titulo=dados.get('titulo'),
        autor=dados.get('autor'),
        sinopse=dados.get('sinopse'),
        genero=genero,
        tipo=tipo,
        capa_url=dados.get('capa_url')
    )

def procedure_remover_livro(livro_id, is_admin=False):
    livro = get_object_or_404(Livro, pk=livro_id)
    if is_admin:
        livro.delete()
    else:
        # Se for usuário comum, talvez apenas marque como indisponível ou similar
        # Mas conforme solicitado: remover livros ( reservado - usuário / excluído - admin )
        livro.delete()

def procedure_atualizar_livro(livro_id, dados):
    livro = get_object_or_404(Livro, pk=livro_id)
    livro.titulo = dados.get('titulo', livro.titulo)
    livro.autor = dados.get('autor', livro.autor)
    livro.sinopse = dados.get('sinopse', livro.sinopse)
    if 'genero_id' in dados:
        livro.genero = get_object_or_404(Genero, pk=dados.get('genero_id'))
    livro.save()
    return livro

# --- Views ---

def index(request):
    livros = Livro.objects.all()[:5]
    return render(request, 'index.html', {'books': livros})

def livraria(request):
    livros = Livro.objects.all()
    return render(request, 'livraria.html', {'books': livros})

def livro_detalhes(request, livro_id):
    livro = get_object_or_404(Livro, pk=livro_id)
    return render(request, 'livro_detalhes.html', {'livro': livro})

@login_required
def reservar_livro(request, livro_id):
    if request.method == 'POST':
        livro = get_object_or_404(Livro, pk=livro_id)
        dias_reserva = int(request.POST.get('dias', 7))
        
        if not livro.reservado:
            data_limite = timezone.now() + timedelta(days=dias_reserva)
            Reserva.objects.create(
                usuario=request.user,
                livro=livro,
                data_limite=data_limite
            )
            livro.reservado = True
            livro.save()
            return redirect('reservas')
    return redirect('livro_detalhes', livro_id=livro_id)

def sobre(request):
    return render(request, 'sobre.html')

def cafeteria(request):
    return render(request, 'cafeteria.html')

def login(request):

    erro = None

    if request.method == 'POST':

        email = request.POST.get('email')
        senha = request.POST.get('senha')

        next_url = request.POST.get('next') or 'index'

        try:

            usuario = User.objects.get(email=email)

            user = authenticate(
                request,
                username=usuario.username,
                password=senha
            )

            if user is not None:

                auth_login(request, user)

                if next_url:
                    return redirect(next_url)

                return redirect('index')

            else:
                erro = 'Senha incorreta.'

        except User.DoesNotExist:
            erro = 'E-mail não encontrado.'

    next_url = request.GET.get('next', '')

    return render(request, 'login.html', {
        'erro': erro,
        'next': next_url
    })

def registro(request):
    erro = None
    if request.method == 'POST':
        nome = request.POST.get('nome')
        email = request.POST.get('email')
        senha = request.POST.get('senha')
        if User.objects.filter(email=email).exists():
            erro = 'Este e-mail já está cadastrado.'
        else:
            user = User.objects.create_user(
                username=email,
                email=email,
                password=senha,
                first_name=nome,
            )
            auth_login(request, user)
            return redirect('index')
    return render(request, 'registro.html', {'erro': erro})

def logout(request):
    auth_logout(request)
    return redirect('login')

@login_required
def reservas(request):
    minhas_reservas = Reserva.objects.filter(usuario=request.user, cancelado=False)
    return render(request, 'reservas.html', {'reservas': minhas_reservas})

@login_required
def cancelar_reserva(request, reserva_id):
    reserva = get_object_or_404(Reserva, id=reserva_id, usuario=request.user)
    reserva.cancelado = True
    reserva.save()
    
    livro = reserva.livro
    livro.reservado = False
    livro.save()
    
    return redirect('reservas')

# =========================
# CAFETERIA
# =========================

def cafeteria(request):

    produtos = Produto.objects.filter(disponivel=True)

    cardapio = {
        'cafe': produtos.filter(categoria='cafe'),
        'gelada': produtos.filter(categoria='gelada'),
        'comida': produtos.filter(categoria='comida'),
        'sobremesa': produtos.filter(categoria='sobremesa'),
    }

    carrinho = request.session.get('carrinho', {})

    total_itens = sum(
        item['quantidade']
        for item in carrinho.values()
    )

    return render(request, 'cafeteria.html', {
        'cardapio': cardapio,
        'total_itens': total_itens,
    })


@login_required
def adicionar_carrinho(request, produto_id):

    if request.method == 'POST':

        produto = Produto.objects.get(id=produto_id)

        carrinho = request.session.get('carrinho', {})

        chave = str(produto_id)

        if chave in carrinho:

            carrinho[chave]['quantidade'] += 1

        else:

            carrinho[chave] = {
                'nome': produto.nome,
                'preco': str(produto.preco),
                'quantidade': 1,
            }

        request.session['carrinho'] = carrinho
        request.session.modified = True

    return redirect('cafeteria')


@login_required
def remover_carrinho(request, produto_id):

    if request.method == 'POST':

        carrinho = request.session.get('carrinho', {})

        chave = str(produto_id)

        if chave in carrinho:

            if carrinho[chave]['quantidade'] > 1:
                carrinho[chave]['quantidade'] -= 1

            else:
                del carrinho[chave]

        request.session['carrinho'] = carrinho
        request.session.modified = True

    return redirect('carrinho')


@login_required
def carrinho(request):

    carrinho = request.session.get('carrinho', {})

    itens = []

    total = Decimal('0')

    for produto_id, item in carrinho.items():

        preco = Decimal(item['preco'])

        quantidade = item['quantidade']

        subtotal = preco * quantidade

        total += subtotal

        itens.append({
            'produto_id': produto_id,
            'nome': item['nome'],
            'preco': preco,
            'quantidade': quantidade,
            'subtotal': subtotal,
        })

    return render(request, 'carrinho.html', {
        'itens': itens,
        'total': total,
    })


@login_required
def finalizar_pedido(request):

    if request.method == 'POST':

        carrinho = request.session.get('carrinho', {})

        if not carrinho:
            return redirect('cafeteria')

        total = Decimal('0')

        for item in carrinho.values():
            total += Decimal(item['preco']) * item['quantidade']

        pedido = Pedido.objects.create(
            usuario=request.user,
            total=total,
            status='confirmado'
        )

        for produto_id, item in carrinho.items():

            produto = Produto.objects.get(id=int(produto_id))

            ItemPedido.objects.create(
                pedido=pedido,
                produto=produto,
                quantidade=item['quantidade'],
                preco_unitario=Decimal(item['preco'])
            )

        request.session['carrinho'] = {}
        request.session.modified = True

        return redirect('meus_pedidos')

    return redirect('carrinho')


@login_required
def meus_pedidos(request):

    pedidos = Pedido.objects.filter(
        usuario=request.user
    ).order_by('-data_pedido').prefetch_related(
        'itens__produto'
    )

    return render(request, 'meus_pedidos.html', {
        'pedidos': pedidos
    })
