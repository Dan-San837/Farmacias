from django.urls import path
from . import views
from .views import seleccionar_sucursal

app_name = 'sales'

urlpatterns = [
    path('', views.index, name='index'),
    path('ventas/', views.ventas_list, name='ventas_list'),                      # Lista de ventas
    path('venta/<int:sucursal_id>/', views.realizar_venta, name='realizar_venta'),  # Realizar venta
    path('ventas/<int:pedido_id>/', views.pedido_detalle, name='detalle_pedido'),   # Ver detalle del pedido
    path('seguimiento/<int:pedido_id>/', views.seguimiento, name='seguimiento'),    # Seguimiento de pedido
    path('seleccionar_sucursal/', seleccionar_sucursal, name='seleccionar_sucursal'),

]
