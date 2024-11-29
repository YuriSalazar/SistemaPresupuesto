from django.urls import path
from .views import AnioApiView, AnioDetails

app_name = "anio"
urlpatterns = [
     path("", AnioApiView.as_view(), name="anio"),#, name='anio'
     path('<int:pk>', AnioDetails.as_view(), name='anio'),
]