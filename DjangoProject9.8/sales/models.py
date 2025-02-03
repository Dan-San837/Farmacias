from django.db import models
from inventory.models import MedicamentoDescrip, Medicamento, Sucursal
from customers.models import Cliente
from django.contrib.auth.models import User


class MedicamentoSucursal(models.Model):
    medicamento = models.ForeignKey(MedicamentoDescrip, on_delete=models.CASCADE)
    sucursal = models.ForeignKey(Sucursal, on_delete=models.CASCADE)
    stock = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.medicamento.nombre} - {self.sucursal.nombre}"

class VentaMedicamento(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    medicamento_sucursal = models.ForeignKey(MedicamentoSucursal, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()
    fecha_venta = models.DateTimeField(auto_now_add=True)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    OPCIONES_ENTREGA = [
        ('retiro', 'Retiro en sucursal'),
        ('envio', 'Envío a sucursal'),
    ]
    tipo_entrega = models.CharField(max_length=10, choices=OPCIONES_ENTREGA)

    def __str__(self):
        return f"Venta: {self.cliente} - {self.medicamento_sucursal.medicamento.nombre}"

class TransferenciaMedicamento(models.Model):
    medicamento_sucursal_origen = models.ForeignKey(MedicamentoSucursal, related_name='origen', on_delete=models.CASCADE)
    medicamento_sucursal_destino = models.ForeignKey(MedicamentoSucursal, related_name='destino', on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()
    fecha_transferencia = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=20, choices=[('pendiente', 'Pendiente'), ('completado', 'Completado')], default='pendiente')

    def __str__(self):
        return f"Transferencia de {self.medicamento_sucursal_origen.medicamento.nombre} - {self.estado}"

class Pedido(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    sucursal_origen = models.ForeignKey(Sucursal, on_delete=models.CASCADE, related_name='sucursal_origen')
    sucursal_destino = models.ForeignKey(Sucursal, on_delete=models.CASCADE, related_name='sucursal_destino', null=True, blank=True)
    fecha = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=20, choices=[('pendiente', 'Pendiente'), ('completado', 'Completado')])
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    OPCIONES_ENTREGA = [
        ('retiro', 'Retirar en sucursal'),
        ('envio', 'Envío a otra sucursal'),
    ]
    opcion_entrega = models.CharField(max_length=10, choices=OPCIONES_ENTREGA, default='retiro')
    sucursal_entrega = models.ForeignKey('inventory.Sucursal', on_delete=models.SET_NULL, null=True, blank=True)

    def calcular_total(self):
        if not self.pk:  # Si el pedido no tiene ID aún, retorna 0
            return 0.00
        return sum(detalle.subtotal for detalle in self.detalles.all())  # Asegurar que detalles existan

    def save(self, *args, **kwargs):
        self.total = self.calcular_total()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Pedido {self.id} - {self.get_opcion_entrega_display()}"


class DetallePedido(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name='detalles')
    medicamento = models.ForeignKey(MedicamentoDescrip, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'{self.medicamento.nombre} - {self.cantidad}'
