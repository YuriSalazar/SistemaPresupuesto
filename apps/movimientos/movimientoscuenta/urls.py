from django.urls import path
from .views import (MovimientoCuentaAPIView, MovimientoCuentaDetails, MovimientoCuentaReporte,
                    MovimientoCuentaDetailsReporte, ReporteGastosTotales,ReporteGastosPorGerencia,
                    ReporteGastosPromedioGerencia, GastoTotalPorMes, TresMayoresGastosPorGerencia)

app_name = 'movimientoscuenta'
urlpatterns = [
    path('',MovimientoCuentaAPIView.as_view(), name='movimientoscuenta'),
    path('<int:pk>',MovimientoCuentaDetails.as_view(), name='movimientoscuenta'),
    path('reporte/',MovimientoCuentaReporte.as_view(), name='movimientoscuenta'),
    path('reporte/<int:movimientocuenta_id>',MovimientoCuentaDetailsReporte.as_view(), name='movimientoscuenta'),
    path('reportegastostotales/',ReporteGastosTotales.as_view(), name='movimientoscuenta'),
    path('reportegastosporgerencia/',ReporteGastosPorGerencia.as_view(), name='movimientoscuenta'),
    path('gastopromediogerencia/',ReporteGastosPromedioGerencia.as_view(), name='movimientoscuenta'),
    path('gastototalpormes/',GastoTotalPorMes.as_view(), name='movimientoscuenta'),
    path('Top3GerenciaGasto/',TresMayoresGastosPorGerencia.as_view(), name='movimientoscuenta'),
]