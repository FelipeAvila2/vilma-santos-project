from django.utils.timezone import now
from datetime import datetime
from rest_framework import serializers
from django.db import models

# Create your models here.


class Fornecedor(models.Model):
    nome = models.CharField(max_length=40)
    email = models.CharField(max_length=50)
    phone = models.CharField(max_length=20)
    endereco = models.CharField(max_length=100)
    contato = models.CharField(max_length=40)

    def __str__(self):
        return self.nome



class Produto(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField()
    preco = models.DecimalField(max_digits=10, decimal_places=4)

    def calcular_custo(self):
        # Calculate the total cost based on the sum of ingredient costs
        total_custo = sum([pi.ingrediente.custo * pi.quantidade for pi in self.produtoingrediente_set.all()])
        return total_custo

    def __str__(self):
        return self.nome


class Ingrediente(models.Model):
    TIPOS_DE_UNIDADE = {
        "L": "Litros",
        "Kg": "Quilos",
        "Un": "Unidades",
    }
    nome = models.CharField(max_length=40)
    unidade_de_medida = models.CharField(max_length=2, choices=TIPOS_DE_UNIDADE)
    quantidade = models.DecimalField(max_digits=10, decimal_places=4)  # This is the quantidade field
    custo = models.DecimalField(max_digits=10, decimal_places=4)
    ordens_de_compra = models.ManyToManyField('PurchaseOrder', through='IngredienteOrdemDeCompra')

    def __str__(self):
        return self.nome

class ProdutoIngrediente(models.Model):
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE, null=True, blank=True)
    ingrediente = models.ForeignKey(Ingrediente, on_delete=models.CASCADE)
    quantidade = models.DecimalField(max_digits=10, decimal_places=4)

    def __str__(self):
        return f"{self.produto.nome} - {self.ingrediente.nome}"


class IngredienteOrdemDeCompra(models.Model):
    ingrediente = models.ForeignKey(Ingrediente, on_delete=models.CASCADE)
    ordem_de_compra = models.ForeignKey('PurchaseOrder', on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=10, decimal_places=4)

    def __str__(self):
        return f"{self.ingrediente.nome} - {self.ordem_de_compra.order_number}"


class PurchaseOrder(models.Model):
    STATUS_CHOICES = {
        "P": "Pendente",
        "R": "Recebido",
        "PG": "Pago",
    }

    # Define your PurchaseOrder model fields
    order_number = models.CharField(max_length=20, unique=True)
    supplier = models.ForeignKey('Fornecedor', on_delete=models.CASCADE)
    order_date = models.DateField(default=now)
    delivery_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pendente')



    # other fields for your PurchaseOrder model

    def save(self, *args, **kwargs):
        if not self.order_number:
            # Generate the order number based on some logic
            # For example, you can use a combination of current date and a sequential number
            current_date = datetime.now().strftime('%Y%m%d')
            last_order = PurchaseOrder.objects.all().order_by('-id').first()
            if last_order:
                last_order_number = int(last_order.order_number[-4:])
                new_order_number = current_date + str(last_order_number + 1).zfill(4)
            else:
                new_order_number = current_date + '0001'
            self.order_number = new_order_number
        super(PurchaseOrder, self).save(*args, **kwargs)

    def __str__(self):
        return self.order_number



class InventoryTransaction(models.Model):
    TRANSACTION_TYPE_CHOICES = {
        "T": "Transferencia",
        "Rc": "Recebido",
        "A": "Ajuste",
        "Rt": "Retorno",
        "D": "Descartado",
        "V": "Venda",
    }

    # Define your InventoryTransaction model fields
    transaction_number = models.CharField(max_length=20, unique=True)
    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPE_CHOICES)
    transaction_date = models.DateField(default=now)
    product = models.ForeignKey('Produto', on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=10, decimal_places=4)
    # other fields for your InventoryTransaction model

    def save(self, *args, **kwargs):
        if not self.transaction_number:
            # Generate the transaction number based on some logic
            # For example, you can use a combination of current date and a sequential number
            current_date = datetime.now().strftime('%Y%m%d')
            last_transaction = InventoryTransaction.objects.all().order_by('-id').first()
            if last_transaction:
                last_transaction_number = int(last_transaction.transaction_number[-4:])
                new_transaction_number = current_date + str(last_transaction_number + 1).zfill(4)
            else:
                new_transaction_number = current_date + '0001'
            self.transaction_number = new_transaction_number
        super(InventoryTransaction, self).save(*args, **kwargs)

    def __str__(self):
        return self.transaction_number


class IngredientTransaction(models.Model):
    TRANSACTION_TYPE_CHOICES = {
        "T": "Transferencia",
        "Rc": "Recebido",
        "A": "Ajuste",
        "Rt": "Retorno",
        "D": "Descartado",
        "U": "Usado",
    }

    # Define your InventoryTransaction model fields
    transaction_number = models.CharField(max_length=20, unique=True)
    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPE_CHOICES)
    transaction_date = models.DateField(default=now)
    ingredient = models.ForeignKey('Ingrediente', on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=10, decimal_places=4)
    # other fields for your InventoryTransaction model

    def save(self, *args, **kwargs):
        if not self.transaction_number:
            # Generate the transaction number based on some logic
            # For example, you can use a combination of current date and a sequential number
            current_date = datetime.now().strftime('%Y%m%d')
            last_transaction = InventoryTransaction.objects.all().order_by('-id').first()
            if last_transaction:
                last_transaction_number = int(last_transaction.transaction_number[-4:])
                new_transaction_number = current_date + str(last_transaction_number + 1).zfill(4)
            else:
                new_transaction_number = current_date + '0001'
            self.transaction_number = new_transaction_number
        super(IngredientTransaction, self).save(*args, **kwargs)

    def __str__(self):
        return self.transaction_number


class IngredienteOrdemDeCompraSerializer(serializers.ModelSerializer):
    nome = serializers.CharField(source='ingrediente.nome', read_only=True)
    custo = serializers.DecimalField(source='ingrediente.custo', read_only=True, max_digits=10, decimal_places=4)

    class Meta:
        model = IngredienteOrdemDeCompra
        fields = ['ingrediente', 'nome', 'quantity', 'custo']  # Add any other fields you want to include