from django.urls import path
from . import views

app_name = 'customers'

urlpatterns = [
    path('', views.lista_clientes, name='lista_clientes'),
    path('perfil/<int:cliente_id>/', views.perfil_cliente, name='perfil_cliente_especifico'),
    path('crear/', views.crear_cliente, name='crear_cliente'),
    path('perfil/', views.perfil_cliente, name='perfil_cliente'),
    path('editar/<int:cliente_id>/', views.editar_perfil, name='editar_perfil'),
]
