from rest_framework.serializers import ModelSerializer
from .models import Gerencia

class GerenciaSerializer(ModelSerializer):
    class Meta:
        model = Gerencia
        fields=['codigo','descripcion','activo','estado','responsable']
        #fields = '__all__'