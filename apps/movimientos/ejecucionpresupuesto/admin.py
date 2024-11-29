from django.contrib import admin
from apps.movimientos.ejecucionpresupuesto.models import EjecucionPresupuesto, DetalleEjecucionPresupuesto

@admin.register(EjecucionPresupuesto)
class EjecucionPresupuestoAdmin(admin.ModelAdmin):
    search_fields = ['presupuesto', 'gerencia', 'cuenta']
    list_display = ['presupuesto', 'gerencia', 'cuenta', 'usuario']

@admin.register(DetalleEjecucionPresupuesto)
class DetalleEjecucionPresupuestoAdmin(admin.ModelAdmin):
    search_fields = ['mes', 'justificacion']
    list_display = ['mes', 'montoreal', 'justificacion']
# Register your models here.
