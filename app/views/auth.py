"""
Views de autenticação: login, registro e logout.
"""

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.models import User
from app.models import Perfil


def login(request):
    """Exibe o formulário de login e autentica o usuário pelo e-mail."""
    if request.user.is_authenticated:
        return redirect('index')

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
    """Exibe o formulário de registro e cria um novo usuário com perfil detalhado."""
    if request.user.is_authenticated:
        return redirect('index')

    erro = None
    if request.method == 'POST':
        # Captura de dados do formulário
        primeiro_nome = request.POST.get('nome')
        sobrenome = request.POST.get('sobrenome')
        data_nascimento = request.POST.get('data_nascimento')
        email = request.POST.get('email')
        telefone = request.POST.get('telefone')
        endereco = request.POST.get('endereco')
        senha = request.POST.get('senha')
        confirmar_senha = request.POST.get('confirmar_senha')

        # Validações básicas
        if not all([primeiro_nome, sobrenome, email, senha, confirmar_senha]):
            erro = 'Os campos obrigatórios devem ser preenchidos.'
        elif senha != confirmar_senha:
            erro = 'As senhas não coincidem.'
        elif User.objects.filter(email=email).exists():
            erro = 'Este e-mail já está cadastrado.'
        else:
            try:
                # Criando o usuário principal
                user = User.objects.create_user(
                    username=email,
                    email=email,
                    password=senha,
                    first_name=primeiro_nome,
                    last_name=sobrenome
                )
                
                # Criando o perfil associado
                Perfil.objects.create(
                    usuario=user,
                    sobrenome=sobrenome,
                    data_nascimento=data_nascimento if data_nascimento else None,
                    telefone=telefone,
                    endereco=endereco
                )

                auth_login(request, user)
                return redirect('index')
            except Exception as e:
                erro = f'Ocorreu um erro ao criar sua conta: {str(e)}'

    return render(request, 'registro.html', {'erro': erro})


def logout(request):
    """Encerra a sessão do usuário e redireciona para o login."""
    auth_logout(request)
    return redirect('login')


from django.contrib.auth.decorators import login_required

@login_required
def perfil(request):
    """Exibe e permite editar os dados do perfil do usuário, incluindo foto."""
    user = request.user
    perfil = user.perfil
    mensagem = None

    if request.method == 'POST':
        user.first_name = request.POST.get('nome')
        perfil.sobrenome = request.POST.get('sobrenome')
        perfil.telefone = request.POST.get('telefone')
        perfil.endereco = request.POST.get('endereco')
        
        if 'foto' in request.FILES:
            perfil.foto = request.FILES['foto']
            
        user.save()
        perfil.save()
        mensagem = "Perfil atualizado com sucesso!"

    return render(request, 'perfil.html', {'perfil': perfil, 'mensagem': mensagem})


@login_required
def pedidos(request):
    """Exibe o histórico de pedidos/consumo na cafeteria (placeholder)."""
    return render(request, 'meus_pedidos.html')


@login_required
def configuracoes(request):
    """Exibe as configurações da conta (placeholder)."""
    return render(request, 'configuracoes.html')
