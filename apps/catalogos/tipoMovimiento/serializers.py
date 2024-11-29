from rest_framework.serializers import ModelSerializer
from .models import TipoMovimiento

class TipoMovimientoSerializer(ModelSerializer):
    class Meta:
        model = TipoMovimiento
        fields=['codigo','descripcion']
        #fields = '__all__'