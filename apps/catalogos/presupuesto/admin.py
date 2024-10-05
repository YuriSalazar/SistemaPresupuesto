from django.contrib import admin
from apps.catalogos.presupuesto.models import Presupuesto

@admin.register(Presupuesto)
class PresupuestoAdmin(admin.ModelAdmin):
    search_fields = ['codigo', 'descripcion', 'activo']
    list_display = ['codigo', 'descripcion', 'fechaInicio', 'fechaFin', 'activo']
# Register your models here.
