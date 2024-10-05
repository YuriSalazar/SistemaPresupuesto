from django.db import models
from apps.catalogos.anio.models import Anio

class Presupuesto(models.Model):
    codigo = models.CharField(verbose_name='Codigo', max_length=30, unique=True)
    descripcion = models.CharField(verbose_name='Descripcion', max_length=50)
    fechaInicio = models.DateField(verbose_name='Fecha Inicio')
    fechaFin = models.DateField(verbose_name='Fecha Fin')
    activo = models.SmallIntegerField(verbose_name='Activo', default=1)
    estado = models.SmallIntegerField(verbose_name='Estado', default=1)
    anio = models.ForeignKey(Anio, verbose_name='Anio', on_delete=models.PROTECT)

    class Meta:
        verbose_name_plural = 'Presupuestos'
    def __str__(self):
        return f"{self.codigo} - {self.descripcion} - {self.fechaInicio} - {self.fechaFin} - {self.activo}"
# Create your models here.
