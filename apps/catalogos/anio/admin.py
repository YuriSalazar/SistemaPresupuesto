from django.contrib import admin
from apps.catalogos.anio.models import Anio

@admin.register(Anio)
class AnioAdmin(admin.ModelAdmin):
    search_fields = ['codigo', 'anio']
    list_display = ['id','codigo', 'anio']
# Register your models here.
