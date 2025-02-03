from django.db import models

# Create your models here.
class Sucursal(models.Model):
    nombre = models.CharField(max_length=100)
    direccion = models.TextField()
    telefono = models.CharField(max_length=15)

    def __str__(self):
        return self.nombre

class Medicamento(models.Model):
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField(default=0)
    sucursal = models.ForeignKey(
        Sucursal,
        on_delete=models.CASCADE,
        related_name="medicamentos",
        default=1  # Cambia este valor por el ID de una sucursal válida
    )

    def __str__(self):
        return self.nombre

class Inventario(models.Model):
    sucursal = models.ForeignKey(Sucursal, on_delete=models.CASCADE)
    medicamento = models.ForeignKey(Medicamento, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ('sucursal', 'medicamento')

    def __str__(self):
        return f'{self.sucursal} - {self.medicamento} - {self.cantidad}'


class MedicamentoDescrip(models.Model):
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True)

    def __str__(self):
        return f"{self.nombre} - {self.descripcion}"