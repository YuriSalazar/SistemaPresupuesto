from django.db import models
"""
Mes
"""
class Mes(models.Model):
    codigo = models.CharField(verbose_name='Codigo', max_length=2, unique=True)
    descripcion = models.CharField(verbose_name='Descripcion', max_length=50)
    class Meta:
        verbose_name_plural = 'Meses'
        # permissions = [
        #     ("puede_aprobar", "Puede aprobar registros"),
        #     ("puede_rechazar", "Puede recharse registros"),
        # ]

    def __str__(self):
        return f"{self.codigo} - {self.descripcion}"

# Create your models here.
