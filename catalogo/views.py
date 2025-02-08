from django.shortcuts import render
from catalogo.models import Produto

def list_products(request):
    filtro = request.GET.get("filtro", "")

    if filtro == "frete_gratis":
        produtos = Produto.objects.filter(frete_gratis=True)
    elif filtro == "full":
        produtos = Produto.objects.filter(tipo_entrega="Full")
    elif filtro == "maior_preco":
        produtos = Produto.objects.order_by("-preco")
    elif filtro == "menor_preco":
        produtos = Produto.objects.order_by("preco")
    elif filtro == "maior_desconto":
        produtos = Produto.objects.order_by("-percentual_desconto")
    else:
        produtos = Produto.objects.all()

    return render(request, "catalogo/list_products.html", {"produtos": produtos})
