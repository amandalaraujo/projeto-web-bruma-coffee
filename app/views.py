from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, 'index.html')

def sobre(request):
    return render(request, 'sobre.html')

def cafeteria(request):
    return render(request, 'cafeteria.html')

def livraria(request):
    return render(request, 'livraria.html')
