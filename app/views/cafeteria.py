from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from decimal import Decimal
from app.models import Produto, Pedido, ItemPedido

def cafeteria(request):
    produtos = Produto.objects.filter(disponivel=True)
    cardapio = {
        'cafe': produtos.filter(categoria='cafe'),
        'gelada': produtos.filter(categoria='gelada'),
        'comida': produtos.filter(categoria='comida'),
        'sobremesa': produtos.filter(categoria='sobremesa'),
    }
    carrinho = request.session.get('carrinho', {})
    total_itens = sum(item['quantidade'] for item in carrinho.values())
    return render(request, 'cafeteria.html', {
        'cardapio': cardapio,
        'total_itens': total_itens,
    })

@login_required
def adicionar_carrinho(request, produto_id):
    if request.method == 'POST':
        produto = get_object_or_404(Produto, id=produto_id)
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
            produto = get_object_or_404(Produto, id=int(produto_id))
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
    pedidos = Pedido.objects.filter(usuario=request.user).order_by('-data_pedido').prefetch_related('itens__produto')
    return render(request, 'meus_pedidos.html', {'pedidos': pedidos})
