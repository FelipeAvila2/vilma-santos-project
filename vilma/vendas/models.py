from django.db import models
from producao.models import Estoque
from inventorio.models import Produto

# Create your models here.

class Cliente(models.Model):
    nome = models.CharField(max_length=40)
    email = models.CharField(max_length=50)
    phone = models.CharField(max_length=20)
    endereco = models.CharField(max_length=100)
    contato = models.CharField(max_length=40)

    def __str__(self):
        return self.nome


class Venda(models.Model):
    estoque = models.ForeignKey(Estoque, on_delete=models.CASCADE, null=True, blank=True)
    cliente = models.ForeignKey('Cliente', null=True, on_delete=models.CASCADE)
    data_de_venda = models.DateField(null=True, auto_now_add=True)
    quantidade = models.IntegerField()
    desconto = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    preco = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.pk:  # If this is a new instance
            self.preco = self.calcular_preco()  # Calculate the price before saving
        super().save(*args, **kwargs)

    def calcular_preco(self):
        product_price = self.produto.price
        total_cost = product_price * self.quantidade
        discounted_cost = total_cost * (1 - self.desconto)
        return discounted_cost

    def calcular_custo(self):
        total_custo = sum(
            [pi.ingrediente.custo * pi.quantidade for pi in self.estoque.produto.produtoingrediente_set.all()])
        return total_custo

    @property
    def lucro_operacional(self):
        return self.preco - self.calcular_custo()

    def __str__(self):
        return f"{self.estoque.produto.nome} - Quantidade: {self.quantidade}"


class Orcamento(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Budget Proposal {self.pk}"


class BudgetProposalItem(models.Model):
    proposal = models.ForeignKey(Orcamento, on_delete=models.CASCADE)
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    quantidade = models.PositiveIntegerField()
    desconto = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def cost(self):
        product_price = self.produto.preco
        total_cost = product_price * self.quantidade
        discounted_cost = total_cost * (1 - self.desconto)
        return discounted_cost

    @property
    def product_price(self):
        return self.produto.preco

    def __str__(self):
        return f"{self.quantidade} x {self.produto.nome} in Budget Proposal {self.proposal.pk}"


