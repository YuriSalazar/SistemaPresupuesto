from django.urls import path, include

urlpatterns = [
    path('movimientoscuenta/', include('apps.movimientos.movimientoscuenta.urls')),
    path('ejecucionpresupuesto/', include('apps.movimientos.ejecucionpresupuesto.urls')),
]