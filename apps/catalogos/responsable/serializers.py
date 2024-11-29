from rest_framework.serializers import ModelSerializer
from .models import Responsable

class ResponsableSerializer(ModelSerializer):
    class Meta:
        model = Responsable
        fields=['codigo','cedula','nombreCompleto','correo','telefono','activo','estado']
        #fields = '__all__'