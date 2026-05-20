"""
Views relacionadas ao fluxo de reservas: criar, listar e cancelar reservas.
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from datetime import timedelta

from app.models import Livro, Reserva


@login_required
def reservar_livro(request, livro_id):
    """
    Processa a solicitação de reserva de um livro.

    Ao confirmar a reserva (POST), cria o registro em `Reserva` e marca
    o campo `reservado` do livro como `True`, garantindo que a tabela de
    livros reflita corretamente a indisponibilidade do exemplar.
    """
    if request.method == 'POST':
        livro = get_object_or_404(Livro, pk=livro_id)
        dias_reserva = int(request.POST.get('dias', 7))

        if livro.reservado:
            messages.warning(
                request,
                f'O livro "{livro.titulo}" já está reservado por outro usuário.',
            )
            return redirect('livro_detalhes', livro_id=livro_id)

        data_limite = timezone.now() + timedelta(days=dias_reserva)

        # Cria o registro de reserva
        Reserva.objects.create(
            usuario=request.user,
            livro=livro,
            data_limite=data_limite,
        )

        # Atualiza o status do livro no banco de dados
        livro.reservado = True
        livro.save(update_fields=['reservado'])

        messages.success(
            request,
            f'Livro "{livro.titulo}" reservado com sucesso por {dias_reserva} dia(s)!',
        )
        return redirect('reservas')

    return redirect('livro_detalhes', livro_id=livro_id)


@login_required
def lista_reservas(request):
    """Lista as reservas ativas e os livros favoritos do usuário autenticado."""
    minhas_reservas = Reserva.objects.filter(
        usuario=request.user,
        cancelado=False,
    ).select_related('livro')
    meus_favoritos = request.user.livros_favoritos.all()
    return render(request, 'reservas.html', {
        'reservas': minhas_reservas,
        'favoritos': meus_favoritos,
    })


@login_required
def cancelar_reserva(request, reserva_id):
    """
    Cancela uma reserva existente do usuário autenticado.

    Marca a reserva como cancelada e libera o livro, atualizando o campo
    `reservado` para `False` na tabela de livros.
    """
    reserva = get_object_or_404(Reserva, id=reserva_id, usuario=request.user)

    # Marca a reserva como cancelada
    reserva.cancelado = True
    reserva.save(update_fields=['cancelado'])

    # Libera o livro no banco de dados
    livro = reserva.livro
    livro.reservado = False
    livro.save(update_fields=['reservado'])

    messages.info(request, 'Reserva cancelada com sucesso.')
    return redirect('reservas')
