from django.urls import path
from .views import TipoMovimientoApiView, TipoMovimientoDetails

app_name = "tipoMovimiento"
urlpatterns = [
     path('', TipoMovimientoApiView.as_view(), name='tipoMovimiento'), # , name='tipoMovimiento'
     path('<int:pk>', TipoMovimientoDetails.as_view(), name='tipoMovimiento')
]