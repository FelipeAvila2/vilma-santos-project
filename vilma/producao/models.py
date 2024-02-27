from django.db import models
from inventorio.models import Produto

# Create your models here.

class Estoque(models.Model):
    # produto_id
    # quantidade
    # data_de_validade
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE, null=True, blank=True)
    quantidade = models.IntegerField()
    data_de_validade = models.DateField()

    def __str__(self):
        return str(self.produto) + " Validade: " + str(self.data_de_validade)

