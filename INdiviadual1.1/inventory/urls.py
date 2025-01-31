from django.urls import path
from . import views

app_name = 'inventory'

urlpatterns = [
    path('', views.inventario_list, name='inventario_list'),         # Ver inventario por sucursal
    path('<int:sucursal_id>/', views.inventario_detail, name='inventario_detail'),  # Detalle de inventario
    path('add/', views.add_medicamento, name='add_medicamento'),    # Agregar medicamento
    path('update/<int:pk>/', views.update_medicamento, name='update_medicamento'),  # Actualizar medicamento
    #path('', views.index, name='index'),
]
