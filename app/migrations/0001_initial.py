# Generated unified migration for Bruma and Coffee & Stack Sisters

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Genero',
            fields=[
                ('codigo', models.IntegerField(primary_key=True, serialize=False)),
                ('nome', models.CharField(max_length=100)),
            ],
            options={
                'verbose_name': 'Gênero',
                'verbose_name_plural': 'Gêneros',
                'ordering': ['nome'],
            },
        ),
        migrations.CreateModel(
            name='Produto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=100)),
                ('descricao', models.CharField(max_length=200)),
                ('preco', models.DecimalField(decimal_places=2, max_digits=6)),
                ('categoria', models.CharField(choices=[('cafe', 'Cafés'), ('gelada', 'Bebidas Geladas'), ('comida', 'Comidas'), ('sobremesa', 'Sobremesas')], max_length=20)),
                ('disponivel', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name': 'Produto',
                'verbose_name_plural': 'Produtos',
            },
        ),
        migrations.CreateModel(
            name='Tipo',
            fields=[
                ('codigo', models.IntegerField(primary_key=True, serialize=False)),
                ('nome', models.CharField(max_length=100)),
            ],
            options={
                'verbose_name': 'Tipo',
                'verbose_name_plural': 'Tipos',
                'ordering': ['nome'],
            },
        ),
        migrations.CreateModel(
            name='Pedido',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data_pedido', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(choices=[('pendente', 'Pendente'), ('confirmado', 'Confirmado'), ('cancelado', 'Cancelado')], default='pendente', max_length=20)),
                ('total', models.DecimalField(decimal_places=2, default=0, max_digits=8)),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Pedido',
                'verbose_name_plural': 'Pedidos',
            },
        ),
        migrations.CreateModel(
            name='ItemPedido',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantidade', models.IntegerField(default=1)),
                ('preco_unitario', models.DecimalField(decimal_places=2, max_digits=6)),
                ('pedido', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='itens', to='app.pedido')),
                ('produto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.produto')),
            ],
        ),
        migrations.CreateModel(
            name='Livro',
            fields=[
                ('codigo', models.IntegerField(primary_key=True, serialize=False)),
                ('titulo', models.CharField(max_length=200)),
                ('autor', models.CharField(max_length=200)),
                ('sinopse', models.TextField()),
                ('reservado', models.BooleanField(default=False)),
                ('capa_url', models.URLField(blank=True, null=True)),
                ('favoritado_por', models.ManyToManyField(blank=True, related_name='livros_favoritos', to=settings.AUTH_USER_MODEL)),
                ('genero', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='livros', to='app.genero')),
                ('tipo', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='app.tipo')),
            ],
            options={
                'verbose_name': 'Livro',
                'verbose_name_plural': 'Livros',
                'ordering': ['titulo'],
            },
        ),
        migrations.CreateModel(
            name='Perfil',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sobrenome', models.CharField(max_length=150)),
                ('data_nascimento', models.DateField(blank=True, null=True)),
                ('telefone', models.CharField(blank=True, max_length=20)),
                ('endereco', models.TextField(blank=True)),
                ('usuario', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='perfil', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Perfil',
                'verbose_name_plural': 'Perfis',
            },
        ),
        migrations.CreateModel(
            name='Reserva',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data_emprestimo', models.DateTimeField(auto_now_add=True)),
                ('data_devolucao', models.DateTimeField(blank=True, null=True)),
                ('data_limite', models.DateTimeField()),
                ('taxa', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('cancelado', models.BooleanField(default=False)),
                ('livro', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reservas_livro', to='app.livro')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reservas_usuario', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Reserva',
                'verbose_name_plural': 'Reservas',
                'ordering': ['-data_emprestimo'],
            },
        ),
    ]