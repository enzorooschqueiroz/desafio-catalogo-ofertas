from django.db import models

class Produto(models.Model):
    imagem = models.URLField(verbose_name="Imagem do Produto")
    nome = models.CharField(max_length=255, verbose_name="Nome do Produto")
    preco = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Preço do Produto")
    parcelamento = models.CharField(max_length=100, blank=True, null=True, verbose_name="Opção de Parcelamento")
    link = models.URLField(verbose_name="Link do Produto")
    preco_sem_desconto = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, verbose_name="Preço sem Desconto")
    percentual_desconto = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True, verbose_name="Percentual de Desconto")
    tipo_entrega = models.CharField(max_length=50, choices=[("Full", "Full"), ("Normal", "Normal")], verbose_name="Tipo de Entrega")
    frete_gratis = models.BooleanField(default=False, verbose_name="Frete Grátis")

    def __str__(self):
        return self.nome
# Create your models here.
