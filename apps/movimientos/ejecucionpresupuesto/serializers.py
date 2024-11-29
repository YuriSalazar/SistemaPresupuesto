from rest_framework.serializers import ModelSerializer, CharField
from .models import DetalleEjecucionPresupuesto, EjecucionPresupuesto

"""
Serializador de la clase DetalleEjecucionPresupuesto
"""
class DetalleEjecucionPresupuestoSerializer(ModelSerializer):
    mes_descripcion=CharField(source='mes.descripcion', read_only=True)
    class Meta:
        model = DetalleEjecucionPresupuesto
        fields = ['mes','montoreal','justificacion','mes_descripcion']

"""
Serializador de la clase EjecucionPresupuesto
"""
class EjecucionPresupuestoSerializer(ModelSerializer):
    presupuesto_descripcion=CharField(source='presupuesto.descripcion', read_only=True)
    gerencia_descripcion=CharField(source='gerencia.descripcion', read_only=True)
    cuenta_descripcion=CharField(source='cuenta.descripcion', read_only=True)
    usuario_nombre=CharField(source='usuario.username', read_only=True)
    detallesep = DetalleEjecucionPresupuestoSerializer(many=True)
    class Meta:
        model=EjecucionPresupuesto
        fields=['presupuesto', 'presupuesto_descripcion','gerencia','gerencia_descripcion','cuenta','cuenta_descripcion','usuario','usuario_nombre','detallesep']