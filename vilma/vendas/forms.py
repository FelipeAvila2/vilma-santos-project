from django import forms
from django.forms import formset_factory

from .models import Cliente, Venda, Orcamento, BudgetProposalItem


class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['nome', 'email', 'phone', 'endereco', 'contato']


class VendaForm(forms.ModelForm):
    class Meta:
        model = Venda
        fields = ['cliente', 'estoque', 'quantidade']

    def __init__(self, *args, **kwargs):
        super(VendaForm, self).__init__(*args, **kwargs)
        self.fields['estoque'].queryset = self.fields['estoque'].queryset.select_related('produto')


class OrcamentoForm(forms.ModelForm):
    class Meta:
        model = Orcamento
        fields = []  # Assuming you don't want to allow editing any fields directly


class BudgetProposalItemForm(forms.ModelForm):
    class Meta:
        model = BudgetProposalItem
        fields = ['produto', 'quantidade', 'desconto']


BudgetProposalItemFormSet = formset_factory(BudgetProposalItemForm, extra=1)