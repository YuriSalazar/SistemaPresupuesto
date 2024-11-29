from django.urls import path
from .views import ResponsableApiView, ResponsableDetails

app_name = "responsable"
urlpatterns = [
     path('', ResponsableApiView.as_view(), name='responsable'), # , name='responsable'
     path('<int:pk>', ResponsableDetails.as_view(), name='responsable'),
]