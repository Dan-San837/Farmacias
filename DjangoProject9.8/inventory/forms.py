from django import forms
from .models import Medicamento, Sucursal
from sales.models import Pedido

class MedicamentoForm(forms.ModelForm):
    class Meta:
        model = Medicamento  # Conecta el formulario al modelo Medicamento
        fields = ['nombre', 'descripcion', 'precio', 'stock']  # Campos del modelo que se incluirán en el formulario
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'precio': forms.NumberInput(attrs={'class': 'form-control'}),
            'stock': forms.NumberInput(attrs={'class': 'form-control'}),
        }


class PedidoForm(forms.ModelForm):
    sucursal_entrega = forms.ModelChoiceField(
        queryset=Sucursal.objects.all(),
        required=False,  # Lo hacemos opcional para evitar el KeyError
        label="Sucursal de Entrega"
    )

    class Meta:
        model = Pedido
        fields = ['sucursal_entrega', 'opcion_entrega']  # Asegúrate de incluir este campo
