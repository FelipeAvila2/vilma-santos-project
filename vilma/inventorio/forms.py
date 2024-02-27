from django import forms
from .models import (PurchaseOrder, InventoryTransaction, IngredientTransaction,
                     Fornecedor, Ingrediente, Produto, ProdutoIngrediente)
from django.forms import inlineformset_factory, BaseModelFormSet, BaseInlineFormSet

class PurchaseOrderForm(forms.ModelForm):
    # order_number
    # supplier
    # order_date
    # delivery_date
    # status

    class Meta:
        model = PurchaseOrder
        fields = ['order_number', 'supplier', 'order_date', 'delivery_date', 'status']
        exclude = ['order_number']
        # Optionally, you can exclude fields or specify additional widgets or labels


class InventoryTransactionForm(forms.ModelForm):
    # transaction_number
    # transaction_type
    # transaction_date
    # product
    # quantity

    class Meta:
        model = InventoryTransaction
        fields = ['transaction_number', 'transaction_type', 'transaction_date', 'product', 'quantity']
        exclude = ['transaction_number']
        # Optionally, you can exclude fields or specify additional widgets or labels


class IngredientTransactionForm(forms.ModelForm):
    # transaction_number
    # transaction_type
    # transaction_date
    # product
    # quantity

    class Meta:
        model = IngredientTransaction
        fields = ['transaction_number', 'transaction_type', 'transaction_date', 'ingredient', 'quantity']
        # Optionally, you can exclude fields or specify additional widgets or labels


class FornecedorForm(forms.ModelForm):
    # nome
    # email
    # phone
    # endereco
    # contato

    class Meta:
        model = Fornecedor
        fields = ['nome', 'email', 'phone', 'endereco', 'contato']
        # Optionally, you can exclude fields or specify additional widgets or labels


class IngredienteForm(forms.ModelForm):
    # nome
    # quantidade
    # unidade_de_medida
    # fornecedor

    class Meta:
        model = Ingrediente
        fields = ['nome', 'quantidade', 'unidade_de_medida', 'custo']
        # Optionally, you can exclude fields or specify additional widgets or labels

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.fields['unidade_de_medida'].widget = forms.Select(choices=Ingrediente.TIPOS_DE_UNIDADE.items())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['quantidade'].required = False


class ProdutoForm(forms.ModelForm):
    class Meta:
        model = Produto
        fields = ['nome', 'descricao', 'preco']


class BaseIngredienteFormSet(BaseModelFormSet):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.queryset = Ingrediente.objects.none()  # No initial queryset
        self.extra = 1  # Set extra to 0 to prevent displaying extra forms initially


IngredienteFormSet = inlineformset_factory(Produto, ProdutoIngrediente, fields=('ingrediente', 'quantidade'), formset=BaseIngredienteFormSet)
