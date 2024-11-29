from django.urls import path
from .views import GerenciaApiView, GerenciaDetails

app_name = "gerencia"
urlpatterns = [
     path('', GerenciaApiView.as_view(), name='gerencia'), #, name='gerencia'
     path('<int:pk>', GerenciaDetails.as_view(), name='gerencia'),
]