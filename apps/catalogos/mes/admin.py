from django.contrib import admin
from apps.catalogos.mes.models import Mes
@admin.register(Mes)
class MesAdmin(admin.ModelAdmin):
    search_fields = ['codigo', 'descripcion']
    list_display = ['codigo', 'descripcion']
# Register your models here.
