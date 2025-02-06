from django.shortcuts import render
from catalogo.models import Produto

def list_products(request):
    produtos = Produto.objects.all()
    return render(request, "catalogo/list_products.html", {"produtos": produtos})
# Create your views here.
