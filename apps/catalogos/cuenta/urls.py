from django.urls import path
from .views import CuentaApiView, CuentaDetails

app_name = "cuenta"
urlpatterns = [
     path('', CuentaApiView.as_view(), name='cuenta'), # , name='cuenta'
     path('<int:pk>', CuentaDetails.as_view(), name='cuenta')
]