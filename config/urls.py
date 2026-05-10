from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from app import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('registro/', views.registro, name='registro'),
    path('logout/', views.logout, name='logout'),
    path('livraria/', views.livraria, name='livraria'),
    path('cafeteria/', views.cafeteria, name='cafeteria'),
    path('sobre/', views.sobre, name='sobre'),
    path('reservar/', views.reservar, name='reservar'),
    path('reservas/', views.reservas, name='reservas'),
    path('cancelar/<int:reserva_id>/', views.cancelar_reserva, name='cancelar_reserva'),
    path('admin/', admin.site.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) \
  + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


def login(request):
    erro = None
    if request.method == 'POST':
        email = request.POST.get('email')
        senha = request.POST.get('senha')

        # busca usuário pelo email
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
                username=email,  # usa email como username
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

