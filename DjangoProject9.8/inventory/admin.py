from django.contrib import admin
from .models import Sucursal, Medicamento, Inventario

@admin.register(Sucursal)
class SucursalAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'direccion', 'telefono')

@admin.register(Medicamento)
class MedicamentoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'sucursal','descripcion', 'precio')
    list_filter = ('sucursal',)

@admin.register(Inventario)
class InventarioAdmin(admin.ModelAdmin):
    list_display = ('sucursal', 'medicamento', 'cantidad')
