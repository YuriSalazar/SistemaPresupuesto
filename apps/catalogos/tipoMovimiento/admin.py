from django.contrib import admin
from apps.catalogos.tipoMovimiento.models import TipoMovimiento
@admin.register(TipoMovimiento)
class TipoMovimientoAdmin(admin.ModelAdmin):
    search_fields = ['codigo', 'descripcion']
    list_display = ['codigo', 'descripcion']
# Register your models here.
