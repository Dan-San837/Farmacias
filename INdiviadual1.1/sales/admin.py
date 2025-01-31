from django.contrib import admin
from .models import Pedido, DetallePedido

@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ('cliente', 'sucursal_origen', 'sucursal_destino', 'fecha', 'estado', 'total')

@admin.register(DetallePedido)
class DetallePedidoAdmin(admin.ModelAdmin):
    list_display = ('pedido', 'medicamento', 'cantidad', 'subtotal', 'get_usuario')

    def get_usuario(self, obj):
        return obj.pedido.cliente.usuario.username

    get_usuario.short_description = 'Usuario'

