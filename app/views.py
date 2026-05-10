import requests
from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.models import User
from .models import Reserva


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

    # pega os títulos que o usuário logado já reservou
    reservados = []
    if request.user.is_authenticated:
        reservados = list(Reserva.objects.filter(
            usuario=request.user,
            status='reservado'
        ).values_list('titulo', flat=True))

    return render(request, 'index.html', {
        'books': livros_home,
        'reservados': reservados
    })

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
        try:
            usuario = User.objects.get(email=email)
            user = authenticate(request, username=usuario.username, password=senha)
            if user is not None:
                auth_login(request, user)
                return redirect('index')
            else:
                erro = 'Senha incorreta.'
        except User.DoesNotExist:
            erro = 'E-mail não encontrado.'
    return render(request, 'login.html', {'erro': erro})


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


#Verifica se o usuário está logado — se não estiver, manda para o login
#Recebe os dados do livro via POST (título, autor, capa)
#Verifica se o usuário já reservou esse livro para não duplicar
#Salva a reserva no banco
#Redireciona de volta para a home
def reservar(request):
    # só usuário logado pode reservar
    if not request.user.is_authenticated:
        return redirect('login')

    if request.method == 'POST':
        titulo = request.POST.get('titulo')
        autor = request.POST.get('autor')
        capa_url = request.POST.get('capa_url')

        # verifica se o usuário já reservou esse livro
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

    # Adicione o filtro status='reservado'
    reservas = Reserva.objects.filter(
        usuario=request.user,
        status='reservado' 
    ).order_by('-data_reserva')

    return render(request, 'reservas.html', {'reservas': reservas})


def cancelar_reserva(request, reserva_id):
    if not request.user.is_authenticated:
        return redirect('login')

    if request.method == 'POST':
        # busca a reserva — garante que é do usuário logado
        try:
            reserva = Reserva.objects.get(id=reserva_id, usuario=request.user)
            reserva.status = 'cancelado'
            reserva.save()
        except Reserva.DoesNotExist:
            pass

    return redirect('reservas')

def livraria(request):
    return render(request, 'livraria.html')

def login(request):
    return render(request, 'login.html')