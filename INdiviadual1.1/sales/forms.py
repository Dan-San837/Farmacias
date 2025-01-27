from django import forms
from .models import Pedido, DetallePedido
from django.forms.models import inlineformset_factory

class PedidoForm(forms.ModelForm):
    class Meta:
        model = Pedido
        fields = ['cliente', 'sucursal_origen', 'sucursal_destino', 'estado']

DetallePedidoFormSet = inlineformset_factory(
    Pedido,
    DetallePedido,
    fields=['medicamento', 'cantidad', 'subtotal'],
    extra=1,
    can_delete=True
)
