from django.contrib import admin
from apps.movimientos.movimientoscuenta.models import MovimientoCuenta, DetalleMovimientoCuenta

@admin.register(MovimientoCuenta)
class MovimientoCuentaAdmin(admin.ModelAdmin):
    search_fields = ['presupuesto', 'gerencia', 'cuenta']
    list_display = ['presupuesto', 'gerencia', 'cuenta', 'usuario']

@admin.register(DetalleMovimientoCuenta)
class DetalleMovimientoCuentaAdmin(admin.ModelAdmin):
    search_fields = ['mes', 'concepto','monto']
    list_display = ['mes', 'concepto', 'monto']

# Register your models here.


