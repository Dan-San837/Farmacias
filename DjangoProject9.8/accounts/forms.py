from django import forms
from django.contrib.auth.models import User
from sales.models import Sucursal


class RegistroForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label="Contraseña")
    confirmar_password = forms.CharField(widget=forms.PasswordInput, label="Confirmar Contraseña")
    rol = forms.ChoiceField(
        choices=[('cliente', 'Cliente'), ('empleado', 'Empleado'), ('admin', 'Administrador')],
        label="Rol"
    )
    sucursal = forms.ModelChoiceField(
        queryset=Sucursal.objects.all(),
        required=False,
        label="Sucursal (Solo para empleados)"
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirmar_password = cleaned_data.get('confirmar_password')

        if password != confirmar_password:
            raise forms.ValidationError("Las contraseñas no coinciden.")

        return cleaned_data
