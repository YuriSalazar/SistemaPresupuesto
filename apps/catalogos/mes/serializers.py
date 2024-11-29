from rest_framework.serializers import ModelSerializer
from .models import Mes

class MesSerializer(ModelSerializer):
    class Meta:
        model = Mes
        fields=['codigo','descripcion']
        #fields = '__all__'