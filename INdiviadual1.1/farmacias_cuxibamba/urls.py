from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

from customers import views

urlpatterns = [
    path('admin/', admin.site.urls),                  # Panel administrativo
    path('inventory/', include('inventory.urls')),   # URLs de inventario
    path('sales/', include('sales.urls')),           # URLs de ventas
    path('customers/', include('customers.urls')),   # URLs de clientes
    path('accounts/', include('accounts.urls')), # URLs de autenticación
    path ('', TemplateView.as_view(template_name='home.html'), name = 'home'),
    path('', views.index, name='index'),  # Ruta para la vista index
    #path('clientes/', include('customers.urls')),

]



