from django.contrib import admin
from .models import Ingrediente, Produto, Fornecedor, InventoryTransaction, PurchaseOrder,IngredientTransaction

# Register your models here.

# Register your models here.

admin.site.register(Ingrediente)

admin.site.register(Produto)

admin.site.register(Fornecedor)

admin.site.register(InventoryTransaction)

admin.site.register(IngredientTransaction)

admin.site.register(PurchaseOrder)
