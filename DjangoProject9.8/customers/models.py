from django.db import models
from django.contrib.auth.models import User

class Cliente(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name='customers_cliente')
    nombre = models.CharField(max_length=100)
    telefono = models.CharField(max_length=15)
    direccion = models.TextField()
    email = models.EmailField(max_length=255, default='default@example.com')

    def __str__(self):
        return f"{self.nombre} ({self.usuario.username})"
