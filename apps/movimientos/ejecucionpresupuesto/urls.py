from django.urls import path
from .views import EjecucionPresupuestoAPIView, EjeccionPresupuestoDetails

app_name = 'ejecucionpresupuesto'
urlpatterns = [
    path('', EjecucionPresupuestoAPIView.as_view(), name='ejecucionpresupuesto'),
    path('<int:pk>', EjeccionPresupuestoDetails.as_view(), name='ejecucionpresupuesto'),
]