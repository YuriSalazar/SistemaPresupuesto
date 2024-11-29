from django.urls import path
from .views import MesApiView, MesDetails

app_name = "mes"
urlpatterns = [
     path('', MesApiView.as_view(), name='mes'), # , name='mes'
     path('<int:pk>', MesDetails.as_view(), name='mes'),
]