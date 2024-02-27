from django.shortcuts import render, redirect
from .forms import EstoqueForm
from .models import Estoque

# Create your views here.

def cozinhar(request):
    if request.method == 'POST':
        form = EstoqueForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('estoque')  # Replace 'success_url' with the URL you want to redirect to after successful form submission
    else:
        form = EstoqueForm()
    return render(request, 'cozinhar.html', {'form': form})

def lista_estoque(request):
    estoque_items = Estoque.objects.all()  # Retrieve all items from Estoque model
    return render(request, 'estoque.html', {'estoque_items': estoque_items})