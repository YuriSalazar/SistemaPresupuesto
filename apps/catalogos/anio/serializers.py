from rest_framework.serializers import ModelSerializer
from .models import Anio

class AnioSerializer(ModelSerializer):
    class Meta:
        model = Anio
        fields=['codigo','anio']
        #fields = '__all__'