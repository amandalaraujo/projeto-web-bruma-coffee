import requests
from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.models import User
from .models import Reserva
from .models import Reserva, Produto, Pedido, ItemPedido
from decimal import Decimal


def buscar_livros():
    url = "https://api.nytimes.com/svc/books/v3/lists/current/hardcover-fiction.json"
    params = {'api-key': settings.NYT_API_KEY}
    response = requests.get(url, params=params)
    livros = []
    for book in response.json().get('results', {}).get('books', []):
        livros.append({
            'title': book.get('title', 'Sem título').title(),
            'author': book.get('author', 'Desconhecido').title(),
            'cover_url': book.get('book_image', ''),
            'genre': 'Ficção',
            'description': book.get('description', 'Sem descrição')[:120],
        })
    return livros


def index(request):
    livros_home = buscar_livros()[:5]
    reservados = []
    if request.user.is_authenticated:
        reservados = list(Reserva.objects.filter(
            usuario=request.user,
            status='reservado'
        ).values_list('titulo', flat=True))
    return render(request, 'index.html', {'books': livros_home, 'reservados': reservados})


def livraria(request):
    return render(request, 'livraria.html')


def sobre(request):
    return render(request, 'sobre.html')


def cafeteria(request):
    return render(request, 'cafeteria.html')


def login(request):
    erro = None
    if request.method == 'POST':
        email = request.POST.get('email')
        senha = request.POST.get('senha')
        next_url = request.POST.get('next', 'index')  # pega o next do form
        try:
            usuario = User.objects.get(email=email)
            user = authenticate(request, username=usuario.username, password=senha)
            if user is not None:
                auth_login(request, user)
                return redirect(next_url)  # redireciona para onde estava
            else:
                erro = 'Senha incorreta.'
        except User.DoesNotExist:
            erro = 'E-mail não encontrado.'

    next_url = request.GET.get('next', '')  # pega o next da URL
    return render(request, 'login.html', {'erro': erro, 'next': next_url})


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


def reservar(request):
    if not request.user.is_authenticated:
        return redirect('login')
    if request.method == 'POST':
        titulo = request.POST.get('titulo')
        autor = request.POST.get('autor')
        capa_url = request.POST.get('capa_url')
        ja_reservou = Reserva.objects.filter(
            usuario=request.user,
            titulo=titulo,
            status='reservado'
        ).exists()
        if not ja_reservou:
            Reserva.objects.create(
                usuario=request.user,
                titulo=titulo,
                autor=autor,
                capa_url=capa_url,
                status='reservado'
            )
    return redirect('index')


def reservas(request):
    if not request.user.is_authenticated:
        return redirect('login')

    todas = Reserva.objects.filter(
        usuario=request.user
    ).order_by('-data_reserva')

    ativas = todas.filter(status='reservado')
    canceladas = todas.filter(status='cancelado')

    return render(request, 'reservas.html', {
        'ativas': ativas,
        'canceladas': canceladas,
    })


def cancelar_reserva(request, reserva_id):
    if not request.user.is_authenticated:
        return redirect('login')
    if request.method == 'POST':
        try:
            reserva = Reserva.objects.get(id=reserva_id, usuario=request.user)
            reserva.status = 'cancelado'
            reserva.save()
        except Reserva.DoesNotExist:
            pass
    return redirect('reservas')

def cafeteria(request):
    produtos = Produto.objects.filter(disponivel=True)

    # organiza por categoria
    cardapio = {
        'cafe': produtos.filter(categoria='cafe'),
        'gelada': produtos.filter(categoria='gelada'),
        'comida': produtos.filter(categoria='comida'),
        'sobremesa': produtos.filter(categoria='sobremesa'),
    }

    # pega o carrinho da sessão
    carrinho = request.session.get('carrinho', {})
    total_itens = sum(item['quantidade'] for item in carrinho.values())

    return render(request, 'cafeteria.html', {
        'cardapio': cardapio,
        'total_itens': total_itens,
    })


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


def carrinho(request):
    if not request.user.is_authenticated:
        return redirect('login')

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


def finalizar_pedido(request):
    if not request.user.is_authenticated:
        return redirect('login')

    if request.method == 'POST':
        carrinho = request.session.get('carrinho', {})

        if not carrinho:
            return redirect('cafeteria')

        # calcula total
        total = Decimal('0')
        for item in carrinho.values():
            total += Decimal(item['preco']) * item['quantidade']

        # cria o pedido no banco
        pedido = Pedido.objects.create(
            usuario=request.user,
            total=total,
            status='confirmado'
        )

        # cria os itens do pedido
        for produto_id, item in carrinho.items():
            produto = Produto.objects.get(id=int(produto_id))
            ItemPedido.objects.create(
                pedido=pedido,
                produto=produto,
                quantidade=item['quantidade'],
                preco_unitario=Decimal(item['preco'])
            )

        # limpa o carrinho
        request.session['carrinho'] = {}
        request.session.modified = True

        return redirect('meus_pedidos')

    return redirect('carrinho')


def meus_pedidos(request):
    if not request.user.is_authenticated:
        return redirect('login')

    pedidos = Pedido.objects.filter(
        usuario=request.user
    ).order_by('-data_pedido').prefetch_related('itens__produto')

    return render(request, 'meus_pedidos.html', {'pedidos': pedidos})