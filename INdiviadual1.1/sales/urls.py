from django.urls import path
from . import views
from .views import seleccionar_sucursal

app_name = 'sales'

urlpatterns = [
    path('', views.index, name='index'),
    path('ventas/', views.ventas_list, name='ventas_list'),                      # Lista de ventas
    path('venta/<int:sucursal_id>/', views.realizar_venta, name='realizar_venta'),  # Realizar venta
    path('pedido_detalle/<int:pedido_id>/', views.pedido_detalle, name='pedido_detalle'),   # Ver detalle del pedido
    path('seguimiento/<int:pedido_id>/', views.seguimiento, name='seguimiento'),    # Seguimiento de pedido
    path('seleccionar_sucursal/', seleccionar_sucursal, name='seleccionar_sucursal'),
    path('medicamentos_list/', views.medicamentos_list, name = 'medicamentos_list' ),
    path('crear_pedido/', views.crear_pedido, name='crear_pedido'),
    path('seguimiento/', views.seguimiento, name = 'seguimiento'),
    path('actualizar_estado/<int:pedido_id>/', views.actualizar_estado, name='actualizar_estado'),
    #path('transferir_stock/', views.transferir_stock, name ="transferir_stock"),


]
