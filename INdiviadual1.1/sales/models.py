from django.db import models
from customers.models import Cliente
from inventory.models import Sucursal, Medicamento


# Create your models here.
class Pedido(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    sucursal_origen = models.ForeignKey(Sucursal, on_delete=models.CASCADE, related_name='sucursal_origen')
    sucursal_destino = models.ForeignKey(Sucursal, on_delete=models.CASCADE, related_name='sucursal_destino', null=True, blank=True)
    fecha = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=20, choices=[('pendiente', 'Pendiente'), ('completado', 'Completado')])
    total = models.DecimalField(max_digits=10, decimal_places=2)
    OPCIONES_ENTREGA = [
        ('retiro', 'Retirar en sucursal'),
        ('envio', 'Envío a otra sucursal'),
    ]
    opcion_entrega = models.CharField(max_length=10, choices=OPCIONES_ENTREGA, default='retiro')
    sucursal_entrega = models.ForeignKey('inventory.Sucursal', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"Pedido {self.id} - {self.get_opcion_entrega_display()}"


class DetallePedido(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name='detalles')
    medicamento = models.ForeignKey(Medicamento, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'{self.medicamento.nombre} - {self.cantidad}'


class Inventario:
    pass

