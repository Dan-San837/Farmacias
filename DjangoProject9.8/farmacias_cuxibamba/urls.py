from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),                  # Panel administrativo
    path('inventory/', include('inventory.urls')),   # URLs de inventario
    path('sales/', include('sales.urls')),           # urls de ventas
    path('customers/', include('customers.urls')),   # URLs de clientes
    path('accounts/', include('accounts.urls')), # urls de autenticación
    path ('', TemplateView.as_view(template_name='home.html'), name = 'home'),
    path('accounts/', include('django.contrib.auth.urls')),

]



