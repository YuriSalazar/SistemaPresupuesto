from django.db import models

from apps.catalogos.tipoMovimiento.models import TipoMovimiento

"""
Cuenta
"""
class Cuenta(models.Model):
    numeroCuenta = models.CharField(verbose_name='Numero de Cuenta', max_length=50, unique=True)
    descripcion = models.CharField(verbose_name='Descripcion', max_length=100)
    activo = models.SmallIntegerField(verbose_name='Activo', default=1)
    estado = models.SmallIntegerField(verbose_name='Estado', default=1)
    tipoMovimiento = models.ForeignKey(TipoMovimiento, verbose_name='Tipo de Movimiento', on_delete=models.PROTECT)
    class Meta:
        verbose_name_plural = 'Cuentas'
    def __str__(self):
        return f"{self.numeroCuenta} - {self.descripcion} - {self.activo}"
# Create your models here.
