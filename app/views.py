from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Livro, Genero, Reserva, Tipo
from django.utils import timezone
from datetime import timedelta

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
