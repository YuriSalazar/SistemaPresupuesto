from django.urls import path
from .views import (EjecucionPresupuestoAPIView, EjecucionPresupuestoDetails, EjecucionPresupuestoReporte,
                    EjecucionPresupuestoDetailsReporte, ReporteAgrupadoAPIView, CantidadRegistrosPorMes)

app_name = 'ejecucionpresupuesto'
urlpatterns = [
    path('', EjecucionPresupuestoAPIView.as_view(), name='ejecucionpresupuesto'),
    path('<int:pk>', EjecucionPresupuestoDetails.as_view(), name='ejecucionpresupuesto'),
    path('reporte/', EjecucionPresupuestoReporte.as_view(), name='ejecucionpresupuesto'),
    path('reporte/<int:ejecucionpresupuesto_id>', EjecucionPresupuestoDetailsReporte.as_view(), name='ejecucionpresupuesto'),
    path('reporte-agrupado/', ReporteAgrupadoAPIView.as_view(), name='ejecucionpresupuesto'),
    path('registrospormes/', CantidadRegistrosPorMes.as_view(), name='ejecucionpresupuesto'),
]