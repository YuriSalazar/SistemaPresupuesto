from django.db import models

from apps.catalogos.responsable.models import Responsable

"""
Gerencia
"""
class Gerencia(models.Model):
    codigo = models.CharField(verbose_name='Codigo', max_length=2, unique=True)
    descripcion = models.CharField(verbose_name='Descripcion', max_length=50)
    activo = models.SmallIntegerField(verbose_name='Activo', default=1)
    estado = models.SmallIntegerField(verbose_name='Estado', default=1)
    responsable = models.ForeignKey(Responsable, verbose_name='Responsable', on_delete=models.PROTECT)
    class Meta:
        verbose_name_plural = 'Gerencias'
        # permissions = [
        #     ("puede_aprobar", "Puede aprobar registros"),
        #     ("puede_rechazar", "Puede recharse registros"),
        # ]

    def __str__(self):
        return f"{self.codigo} - {self.descripcion} - {self.activo}"

# Create your models here.
