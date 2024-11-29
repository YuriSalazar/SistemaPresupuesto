from django.urls import path
from .views import MovimientoCuentaAPIView, MovimientoCuentaDetails

app_name = 'movimientoscuenta'
urlpatterns = [
    path('',MovimientoCuentaAPIView.as_view(), name='movimientoscuenta'),
    path('<int:pk>',MovimientoCuentaDetails.as_view(), name='movimientoscuenta'),
]