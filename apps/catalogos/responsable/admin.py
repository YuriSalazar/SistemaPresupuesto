from django.contrib import admin
from apps.catalogos.responsable.models import Responsable

@admin.register(Responsable)
class ResponsableAdmin(admin.ModelAdmin):
    search_fields = ['codigo', 'cedula', 'nombreCompleto', 'activo']
    list_display = ['codigo', 'cedula','nombreCompleto', 'correo', 'telefono', 'activo']
# Register your models here.
