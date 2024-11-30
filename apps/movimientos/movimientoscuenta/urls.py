from django.urls import path
from .views import MovimientoCuentaAPIView, MovimientoCuentaDetails, MovimientoCuentaReporte, MovimientoCuentaDetailsReporte

app_name = 'movimientoscuenta'
urlpatterns = [
    path('',MovimientoCuentaAPIView.as_view(), name='movimientoscuenta'),
    path('<int:pk>',MovimientoCuentaDetails.as_view(), name='movimientoscuenta'),
    path('reporte/',MovimientoCuentaReporte.as_view(), name='movimientoscuenta'),
    path('reporte/<int:movimientocuenta_id>',MovimientoCuentaDetailsReporte.as_view(), name='movimientoscuenta'),
]