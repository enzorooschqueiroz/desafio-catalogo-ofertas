from django.contrib import admin
from .models import Produto

@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    list_display = ("nome", "preco", "tipo_entrega", "frete_gratis")
    search_fields = ("nome",)
