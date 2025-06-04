from django.urls import path
from .views import AnioApiView, AnioDetails, AnioCantidad

app_name = "anio"
urlpatterns = [
     path("", AnioApiView.as_view(), name="anio"),#, name='anio'
     path('<int:pk>', AnioDetails.as_view(), name='anio'),
     path('cantidad/', AnioCantidad.as_view(), name='anio-cantidad'),
]