from django.contrib import admin
from apps.catalogos.cuenta.models import Cuenta

@admin.register(Cuenta)
class CuentaAdmin(admin.ModelAdmin):
    search_fields = ['numeroCuenta', 'descripcion', 'activo']
    list_display = ['numeroCuenta', 'descripcion', 'activo']
# Register your models here.
