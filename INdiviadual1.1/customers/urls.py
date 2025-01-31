from django.urls import path
from . import views

app_name = 'customers'

urlpatterns = [
    path('', views.lista_clientes, name='lista_clientes'),
    #path('<int:cliente_id>/', views.detalle_cliente, name='detalle_cliente'),
    path('perfil/<int:cliente_id>/', views.perfil_cliente, name='perfil_cliente'),
    path('crear/', views.crear_cliente, name='crear_cliente'),
    #path('', views.index, name='index'),
    path('perfil/', views.perfil_cliente, name='perfil_cliente'),
    path('editar/<int:cliente_id>/', views.editar_perfil, name='editar_perfil'),
    path('perfil/<int:cliente_id>/', views.perfil_cliente, name='perfil_cliente_especifico'),
]
