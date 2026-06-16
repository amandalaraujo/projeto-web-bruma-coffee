<h1 align="center">
  <img src="https://readme-typing-svg.demolab.com?font=Fira+Code&size=28&pause=1000&color=6F4E37&center=true&vCenter=true&width=500&lines=Bruma+%26+Coffee+%F0%9F%93%9A%E2%98%95" alt="Bruma & Coffee" />
</h1>

<p align="center">
  Sistema Full-Stack transacional integrado que combina a gestão de acervo e reservas de uma biblioteca com o fluxo de vendas de uma cafeteria corporativa.
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white"/>
  <img src="https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white"/>
  <img src="https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white"/>
  <img src="https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white"/>
  <img src="https://img.shields.io/badge/SQLite-07405E?style=for-the-badge&logo=sqlite&logoColor=white"/>
</p>

<p align="center">
  <a href="#-sobre-o-projeto">Sobre</a> •
  <a href="#-funcionalidades">Funcionalidades</a> •
  <a href="#-screenshots">Screenshots</a> •
  <a href="#-tecnologias">Tecnologias</a> •
  <a href="#-como-executar">Como Executar</a> •
  <a href="#-desenvolvedores">Desenvolvedores</a>
</p>

---

## 📌 Sobre o Projeto

O **Bruma & Coffee** foi desenvolvido como trabalho final da disciplina de **Programação Web** do curso de Ciência da Computação. O objetivo foi aplicar na prática o padrão **MVT (Model-View-Template)** nativo do Django, construindo uma aplicação robusta, segura e performática — sem dependência de frameworks ou bibliotecas front-end externas.

A proposta une dois sistemas em um só:
- 📖 **Biblioteca** — catálogo, reservas e controle de acervo
- ☕ **Cafeteria** — cardápio, carrinho de compras e fluxo completo de pedidos

---

## ✨ Funcionalidades

### 🔐 Autenticação e Perfis
- Login, logout e registro com **e-mail como identificador exclusivo**
- Extensão do modelo de usuário do Django via `OneToOneField` → dados extras como foto, telefone e endereço

### 📖 Biblioteca
- Catálogo categorizado por **Gênero** e **Tipo**, com paginação e ordenação
- **Reserva transacional:** alteração de status do livro + cálculo automático do prazo de devolução (7 dias)
- Sistema de **Favoritos** via relacionamento `ManyToManyField`
- **Busca preditiva** com retorno em JSON para autocompletar na interface (`__icontains`)

### ☕ Cafeteria
- Cardápio dividido por categorias: Cafés, Bebidas Geladas, Comidas e Sobremesas
- **Carrinho dinâmico** com persistência em sessões nativas do Django (sem gravações prematuras no banco)
- **Fechamento de pedido:** converte o carrinho em registros reais de `Pedido` e `ItemPedido`, com subtotais e totais calculados automaticamente

### 🛡️ Painel Administrativo
- Admin do Django totalmente customizado
- `TabularInline` para visualização de itens dentro do pedido
- `StackedInline` para perfil acoplado ao cadastro de usuários
- Filtros avançados por categoria, status de reserva e busca otimizada

---

## 🖼️ Screenshots

> Algumas telas do sistema em funcionamento.

### Página Inicial
<img width="1600" height="777" alt="image" src="https://github.com/user-attachments/assets/5d93b79c-f11f-45a9-ac57-97fcefafd58f" />
<img width="1600" height="510" alt="image" src="https://github.com/user-attachments/assets/4e2a0f77-54fd-4eac-b848-3cb1bb84e3cf" />
<img width="1600" height="739" alt="image" src="https://github.com/user-attachments/assets/1da41a9a-c4fe-4b34-a5a9-465e1e078f8a" />
<img width="1600" height="770" alt="image" src="https://github.com/user-attachments/assets/94681371-d6a8-4928-970f-ab20d827f053" />


### Catálogo da Biblioteca
<img width="1600" height="692" alt="image" src="https://github.com/user-attachments/assets/cf9d55f1-64e4-41c5-984d-632821682a17" />
<img width="1600" height="770" alt="image" src="https://github.com/user-attachments/assets/3f208189-e515-44a7-820d-b33fe3b77c26" />


### Reserva de Livros
<img width="1600" height="775" alt="image" src="https://github.com/user-attachments/assets/3f19cd39-039f-4d6f-8a81-ae124f84578e" />


### Cardápio da Cafeteria
<img width="1600" height="690" alt="image" src="https://github.com/user-attachments/assets/77f99002-b372-4304-af66-5958f8affd1f" />
<img width="1600" height="775" alt="image" src="https://github.com/user-attachments/assets/d9f05da7-f10f-4dca-bd42-bc27a0a0280f" />


### Carrinho de Compras
<img width="1600" height="610" alt="image" src="https://github.com/user-attachments/assets/b13fd8cf-1447-4817-a5d9-49083bb7f6e4" />


### Sobre
<img width="1600" height="730" alt="image" src="https://github.com/user-attachments/assets/3af3add0-5998-4e29-aa47-9aa0422c6da0" />
<img width="1600" height="764" alt="image" src="https://github.com/user-attachments/assets/d6b6bca7-a158-479f-81fe-534599a3e9b9" />
<img width="1600" height="774" alt="image" src="https://github.com/user-attachments/assets/c8f3265e-15ad-4d92-a892-3b79011d0f7f" />
<img width="1600" height="702" alt="image" src="https://github.com/user-attachments/assets/f0a6bf07-1b48-4236-9e16-27c2e8590917" />


### Painel Administrativo
<img width="1600" height="598" alt="image" src="https://github.com/user-attachments/assets/cadf74b6-d0f3-4f40-aa69-516c03e84371" />


---

## 🛠️ Tecnologias

| Camada | Tecnologia |
|--------|-----------|
| Back-end | Python + Django (ORM, autenticação nativa, sessões, views por funções) |
| Front-end | HTML5 + CSS3 puros (sem frameworks) |
| Banco de Dados | SQLite com carga inicial via fixtures JSON |
| Design & Modelagem | Figma (prototipagem) · DBdiagram / Workbench (MER/DER) |

### Arquitetura CSS Modular
Cada template possui seu próprio arquivo CSS dedicado. Um arquivo global `style.css` centraliza as diretrizes visuais e garante consistência em todo o ecossistema — sem Bootstrap, sem Tailwind.

---

## 🚀 Como Executar

### Pré-requisitos
- Python 3.10+
- pip

### Passo a Passo

```bash
# 1. Clone o repositório
git clone https://github.com/seu-usuario/bruma-and-coffee.git
cd bruma-and-coffee

# 2. Crie e ative o ambiente virtual
python -m venv venv

# Windows
venv\Scripts\activate

# Linux / Mac
source venv/bin/activate

# 3. Instale as dependências
pip install django

# 4. Execute as migrações
python manage.py migrate

# 5. Popule o banco de dados
python manage.py loaddata livros.json
python manage.py loaddata produtos.json

# 6. Inicie o servidor
python manage.py runserver
```

Acesse em: **http://127.0.0.1:8000/**

---

## 👥 Desenvolvedores

<table align="center">
  <tr>
    <td align="center">
      <a href="https://github.com/amandalaraujo">
        <img src="https://github.com/amandalaraujo.png" width="80px" style="border-radius:50%"/><br/>
        <sub><b>Amanda Araújo</b></sub>
      </a>
    </td>
    <td align="center">
      <a href="https://github.com/Coding-Ayko">
        <img src="https://github.com/Coding-Ayko.png" width="80px" style="border-radius:50%"/><br/>
        <sub><b>Tauane Carolina Miranda</b></sub>
      </a>
    </td>
    <td align="center">
      <a href="https://github.com/gestevees">
        <img src="https://github.com/gestevees.png" width="80px" style="border-radius:50%"/><br/>
        <sub><b>Guilherme Esteves</b></sub>
      </a>
    </td>
  </tr>
</table>

---

<p align="center">
  Projeto acadêmico desenvolvido para a disciplina de <strong>Programação Web</strong> — Ciência da Computação
</p>
