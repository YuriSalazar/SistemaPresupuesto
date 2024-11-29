from rest_framework.serializers import ModelSerializer
from .models import Presupuesto

class PresupuestoSerializer(ModelSerializer):
    class Meta:
        model = Presupuesto
        fields=['codigo','descripcion','fechaInicio','fechaFin','activo','estado','anio']
        #fields = '__all__'