from django.urls import path
from .views import PresupuestoApiView, PresupuestoDetails

app_name = "presupuesto"
urlpatterns = [
     path('', PresupuestoApiView.as_view(), name='presupuesto'), #, name='presupuesto'
     path('<int:pk>', PresupuestoDetails.as_view(), name='presupuesto'),
]