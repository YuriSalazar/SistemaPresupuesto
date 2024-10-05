from django.db import models
"""
Responsable
"""
class Responsable(models.Model):
    codigo = models.CharField(verbose_name='Codigo', max_length=5, unique=True)
    cedula = models.CharField(verbose_name='Cedula', max_length=50)
    nombreCompleto = models.CharField(verbose_name='Nombre Completo', max_length=50)
    correo = models.CharField(verbose_name='Correo', max_length=50)
    telefono = models.CharField(verbose_name='Telefono', max_length=50)
    activo = models.PositiveSmallIntegerField(verbose_name='Activo', default=1)
    estado = models.PositiveSmallIntegerField(verbose_name='Estado', default=1)
    class Meta:
        verbose_name_plural = 'Responsables'

    def __str__(self):
        return f"{self.codigo} - {self.cedula} - {self.nombreCompleto} - {self.correo} - {self.telefono} - {self.activo}"

# Create your models here.
