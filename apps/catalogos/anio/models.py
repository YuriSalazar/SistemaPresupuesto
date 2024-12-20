from django.db import models

"""
Anio
"""
class Anio(models.Model):
    codigo = models.CharField(verbose_name='Codigo', max_length=10, unique=True)
    anio = models.IntegerField(verbose_name='Año', unique=True)
    class Meta:
        verbose_name_plural = 'Años'
        # permissions = [
        #     ("puede_aprobar", "Puede aprobar registros"),
        #     ("puede_rechazar", "Puede recharse registros"),
        # ]

    def __str__(self):
        return f"{self.codigo} - {self.anio}"


# Create your models here.
