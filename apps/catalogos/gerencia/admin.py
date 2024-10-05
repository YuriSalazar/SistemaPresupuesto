from django.contrib import admin
from apps.catalogos.gerencia.models import Gerencia
@admin.register(Gerencia)
class GerenciaAdmin(admin.ModelAdmin):
    search_fields = ['codigo', 'descripcion', 'activo']
    list_display = ['codigo', 'descripcion', 'activo']
# Register your models here.
