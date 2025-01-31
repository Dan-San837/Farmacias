from django.urls import path
from django.contrib.auth.views import LoginView
from . import views
from django.contrib.auth import views as auth_views
from .views import custom_login

app_name = 'accounts'

urlpatterns = [
    path('login/', LoginView.as_view(template_name='accounts/login.html'), name='login'),  # Inicio de sesión
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),                                  # Cierre de sesión
    path('register/', views.register, name='register'),                                              # Registro de usuarios
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),          # Restablecimiento de contraseña
    #path('', views.index, name='index'),
#path('password_reset/', auth_views.PasswordResetView.as_view(template_name='accounts/password_reset.html'), name='password_reset'),
    path('login/', custom_login, name='login'),

]
