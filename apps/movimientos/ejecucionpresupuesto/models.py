from django.db import models
from apps.catalogos.presupuesto.models import Presupuesto
from apps.catalogos.gerencia.models import Gerencia
from apps.seguridad.usuarios.models import User
from apps.catalogos.mes.models import Mes
from apps.catalogos.cuenta.models import Cuenta

# Create your models here.
class EjecucionPresupuesto(models.Model):
    presupuesto = models.ForeignKey(Presupuesto, verbose_name='Presupuesto', on_delete=models.PROTECT)
    gerencia = models.ForeignKey(Gerencia, verbose_name='Gerencia', on_delete=models.PROTECT)
    cuenta=models.ForeignKey(Cuenta, verbose_name='Cuenta', on_delete=models.PROTECT)
    usuario = models.ForeignKey(User, verbose_name='Usuario', on_delete=models.PROTECT)
    estado=models.SmallIntegerField(verbose_name='Estado', default=1)

    class Meta:
        verbose_name_plural = 'Ejecuciones de Presupuesto'

    def __str__(self):
        return f"{self.presupuesto} - {self.gerencia} - {self.cuenta} - {self.usuario}"

class DetalleEjecucionPresupuesto(models.Model):
    ejecucionpresupuesto=models.ForeignKey(EjecucionPresupuesto, related_name='detallesep', on_delete=models.PROTECT)
    mes=models.ForeignKey(Mes, verbose_name='Mes', on_delete=models.PROTECT)
    montoreal=models.DecimalField(verbose_name='Monto real', max_digits=10, decimal_places=2)
    justificacion=models.CharField(verbose_name='Justificacion', max_length=300)
    estado=models.SmallIntegerField(verbose_name='Estado', default=1)

    class Meta:
        verbose_name_plural = 'Detalles de EjecucionPresupuesto'
        # permissions = [
        #     ("puede_aprobar", "Puede aprobar registros"),
        #     ("puede_rechazar", "Puede recharse registros"),
        # ]

    def __str__(self):
        return f"{self.mes} - {self.montoreal} - {self.justificacion}"

