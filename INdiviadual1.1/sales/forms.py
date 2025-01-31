from django import forms
from .models import Pedido, DetallePedido, Sucursal
from django.forms.models import inlineformset_factory

class PedidoForm(forms.ModelForm):
    class Meta:
        model = Pedido
        fields = ['sucursal_entrega', 'opcion_entrega']

    sucursal_entrega = forms.ModelChoiceField(
        queryset=Sucursal.objects.all(),
        required=False,  # Lo hacemos opcional para evitar el KeyError
        label="Sucursal de Entrega"
    )


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['sucursal_entrega'].queryset = Sucursal.objects.all()

    def clean(self):
        cleaned_data = super().clean()
        opcion_entrega = cleaned_data.get('opcion_entrega')
        sucursal_entrega = cleaned_data.get('sucursal_entrega')

        if opcion_entrega == 'envio' and not sucursal_entrega:
            raise forms.ValidationError(
                "Debe seleccionar una sucursal de origen si elige la opción 'Envío desde otra sucursal'.")
        return cleaned_data


DetallePedidoFormSet = inlineformset_factory(
    Pedido,
    DetallePedido,
    fields=['medicamento', 'cantidad', 'subtotal'],
    extra=1,
    can_delete=True
)
