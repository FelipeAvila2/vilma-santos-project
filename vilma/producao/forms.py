from django import forms
from .models import Estoque


class EstoqueForm(forms.ModelForm):
    class Meta:
        model = Estoque
        fields = ['produto', 'quantidade', 'data_de_validade']  # Add other fields from Estoque model as needed

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['data_de_validade'].widget = forms.DateInput(attrs={'type': 'date'})
        # You can customize the form further if needed, such as adding widgets or setting labels