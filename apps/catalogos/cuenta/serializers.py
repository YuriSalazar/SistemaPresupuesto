from rest_framework.serializers import ModelSerializer
from .models import Cuenta

class CuentaSerializer(ModelSerializer):
    class Meta:
        model = Cuenta
        fields=['numeroCuenta','descripcion','activo','estado','tipoMovimiento']
        #fields = '__all__'