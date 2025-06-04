from django.urls import path
from .views import PresupuestoApiView, PresupuestoDetails, PresupuestoCantidad

app_name = "presupuesto"
urlpatterns = [
     path('', PresupuestoApiView.as_view(), name='presupuesto'), #, name='presupuesto'
     path('<int:pk>', PresupuestoDetails.as_view(), name='presupuesto'),
     path('cantidadpresupuesto/', PresupuestoCantidad.as_view(), name='presupuesto'),
]