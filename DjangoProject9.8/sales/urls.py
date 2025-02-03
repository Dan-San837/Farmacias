from django.urls import path
from . import views

app_name='sales'

urlpatterns = [
    path('', views.index, name='index'),
    path('ventas/', views.ventas_list, name='ventas_list'),
    path('venta/<int:sucursal_id>/', views.realizar_venta, name='realizar_venta'),
    path('pedido_detalle/<int:pedido_id>/', views.pedido_detalle, name='pedido_detalle'),
    path('ventas/', views.venta_medicamento, name='ventas'),
    path('transferencias/', views.transferencia_medicamento, name='transferencias'),
    path('crear_pedido/', views.crear_pedido, name='crear_pedido'),
    path('seguimiento/<int:pedido_id>/', views.seguimiento, name='seguimiento'),
    path('seguimiento/', views.seguimiento, name = 'seguimiento'),
    path('medicamentos_list/', views.medicamentos_list, name = 'medicamentos_list' ),
    path('seleccionar_sucursal/', views.seleccionar_sucursal, name='seleccionar_sucursal'),
    path('actualizar_estado/<int:pedido_id>/', views.actualizar_estado, name='actualizar_estado'),
    path('transferencia_medicamento/', views.transferencia_medicamento, name ="transferencia_medicamento"),
      # Realizar venta
]
