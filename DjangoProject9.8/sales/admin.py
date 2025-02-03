from django.contrib import admin
from .models import Pedido, DetallePedido, VentaMedicamento, TransferenciaMedicamento

@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ('cliente', 'sucursal_origen', 'sucursal_destino', 'fecha', 'estado', 'total', 'opcion_entrega', 'sucursal_entrega')
    search_fields = ('cliente__nombre', 'estado')  # Verifica que Cliente tenga 'nombre'
    list_filter = ('estado', 'fecha', 'opcion_entrega')

@admin.register(DetallePedido)
class DetallePedidoAdmin(admin.ModelAdmin):
    list_display = ('pedido', 'get_medicamento', 'cantidad', 'subtotal', 'get_cliente')
    search_fields = ('pedido__cliente__nombre',)  # Cliente debe tener 'nombre'
    list_filter = ('pedido__fecha',)

    def get_cliente(self, obj):
        return obj.pedido.cliente.nombre if obj.pedido.cliente else "Sin cliente"

    get_cliente.short_description = 'Cliente'

    def get_medicamento(self, obj):
        return obj.medicamento.nombre if obj.medicamento else "Noespecificado"

    get_medicamento.short_description = 'Medicamento'


@admin.register(VentaMedicamento)
class VentaMedicamentoAdmin(admin.ModelAdmin):
    list_display = ('cliente', 'get_sucursal', 'get_medicamento', 'cantidad')
    search_fields = ()
    list_filter = ()

    def get_sucursal(self, obj):
        return obj.sucursal.nombre if obj.sucursal else "Noespecificado"

    get_sucursal.short_description = 'Sucursal'

    def get_medicamento(self, obj):
        return obj.medicamento.nombre if obj.medicamento else "Noespecificado"

    get_medicamento.short_description = 'Medicamento'

@admin.register(TransferenciaMedicamento)
class TransferenciaMedicamentoAdmin(admin.ModelAdmin):
    list_display = ('get_sucursal_origen', 'get_sucursal_destino', 'get_medicamento', 'cantidad', 'estado')
    search_fields = ()
    list_filter = ()

    def get_sucursal_origen(self, obj):
        return obj.sucursal_origen.nombre if obj.sucursal_origen else "Noespecificado"

    get_sucursal_origen.short_description = 'Sucursal Origen'

    def get_sucursal_destino(self, obj):
        return obj.sucursal_destino.nombre if obj.sucursal_destino else "Noespecificado"

    get_sucursal_destino.short_description = 'Sucursal Destino'

    def get_medicamento(self, obj):
        return obj.medicamento.nombre if obj.medicamento else "Noespecificado"

    get_medicamento.short_description = 'Medicamento'
