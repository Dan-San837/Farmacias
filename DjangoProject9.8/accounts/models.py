from django.contrib.auth.models import User
from django.db import models
from inventory.models import Sucursal  # Importar Sucursal si EmpleadoSucursal la necesita

class Cliente(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name='accounts_cliente')  # Relación uno a uno con User

    def __str__(self):
        return f'Cliente: {self.usuario.username}'

class EmpleadoSucursal(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)  # Relación uno a uno con User
    sucursal = models.ForeignKey(Sucursal, on_delete=models.CASCADE, null=True, blank=True)  # Relación con Sucursal

    def __str__(self):
        return f'Empleado: {self.usuario.username} - Sucursal: {self.sucursal.nombre if self.sucursal else "No asignada"}'
