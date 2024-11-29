from django.db import models
from apps.catalogos.presupuesto.models import Presupuesto
from apps.catalogos.gerencia.models import Gerencia
from apps.seguridad.usuarios.models import User
from apps.catalogos.mes.models import Mes
from apps.catalogos.cuenta.models import Cuenta

# Create your models here.
class MovimientoCuenta(models.Model):
    presupuesto = models.ForeignKey(Presupuesto, verbose_name='Presupuesto', on_delete=models.PROTECT)
    gerencia = models.ForeignKey(Gerencia, verbose_name='Gerencia' ,on_delete=models.PROTECT)
    cuenta = models.ForeignKey(Cuenta, verbose_name='Cuenta', on_delete=models.PROTECT)
    usuario= models.ForeignKey(User, verbose_name='Usuario' ,on_delete=models.PROTECT)
    estado=models.SmallIntegerField(verbose_name='Estado',default=1)

    class Meta:
        verbose_name_plural = 'Movimientos de Cuentas'

    def __str__(self):
        return f"{self.cuenta} - {self.gerencia} -  {self.presupuesto} - {self.usuario}"

class DetalleMovimientoCuenta(models.Model):
    movimientocuenta=models.ForeignKey(MovimientoCuenta, related_name='detallesmc', on_delete=models.PROTECT)
    mes= models.ForeignKey(Mes, verbose_name='Mes', on_delete=models.PROTECT)
    concepto=models.CharField(verbose_name='Concepto', max_length=200)
    monto=models.DecimalField(verbose_name='Monto',decimal_places=2,max_digits=10)
    estado=models.SmallIntegerField(verbose_name='Estado',default=1)

    class Meta:
        verbose_name_plural = 'Detalles de Movimientos Cuentas'
        # permissions = [
        #     ("puede_aprobar", "Puede aprobar registros"),
        #     ("puede_rechazar", "Puede recharse registros"),
        # ]

    def __str__(self):
        return f"{self.mes} - {self.concepto} - {self.monto}"