from django.urls import path, include

urlpatterns = [
    path('anio/', include('apps.catalogos.anio.urls')),
    path('cuenta/', include('apps.catalogos.cuenta.urls')),
    path('gerencia/', include('apps.catalogos.gerencia.urls')),
    path('mes/', include('apps.catalogos.mes.urls')),
    path('presupuesto/', include('apps.catalogos.presupuesto.urls')),
    path('responsable/', include('apps.catalogos.responsable.urls')),
    path('tipoMovimiento/', include('apps.catalogos.tipoMovimiento.urls')),
]