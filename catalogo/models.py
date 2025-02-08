from django.db import models

class ProdutoManager(models.Manager):
    def com_frete_gratis(self):
        return self.filter(frete_gratis=True)

    def entregues_pelo_full(self):
        return self.filter(tipo_entrega="Full")

    def maior_preco(self):
        return self.order_by("-preco")

    def menor_preco(self):
        return self.order_by("preco")

    def maior_desconto(self):
        return self.order_by("-percentual_desconto")

class Produto(models.Model):
    imagem = models.URLField(verbose_name="Imagem do Produto")
    nome = models.CharField(max_length=500, verbose_name="Nome do Produto")  # Aumentado
    preco = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Preço do Produto")
    parcelamento = models.CharField(max_length=1000, blank=True, null=True, verbose_name="Opção de Parcelamento")  # Aumentado
    link = models.CharField(max_length=1000)  # Aumentado
    preco_sem_desconto = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True, verbose_name="Preço sem Desconto")
    percentual_desconto = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True, verbose_name="Percentual de Desconto")
    tipo_entrega = models.CharField(max_length=100, choices=[("Full", "Full"), ("Normal", "Normal")], verbose_name="Tipo de Entrega")  # Aumentado
    frete_gratis = models.BooleanField(default=False, verbose_name="Frete Grátis")

    def __str__(self):
        return self.nome
# Create your models here.
