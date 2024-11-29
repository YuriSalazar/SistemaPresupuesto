from rest_framework.serializers import ModelSerializer, CharField
from .models import DetalleMovimientoCuenta, MovimientoCuenta

"""
Serializador de la clase DetalleMovimientoCuenta
"""
class DetalleMovimientoCuentaSerializer(ModelSerializer):
    mes_descripcion = CharField(source='mes.descripcion', read_only=True)
    class Meta:
        model = DetalleMovimientoCuenta
        fields = ['mes','mes_descripcion','concepto','monto']

"""
Serializador de la clase MovimientoCuenta
"""
class MovimientoCuentaSerializer(ModelSerializer):
    presupuesto_descripcion=CharField(source='presupuesto.descripcion', read_only=True)
    gerencia_descripcion=CharField(source='gerencia.descripcion', read_only=True)
    cuenta_descripcion=CharField(source='cuenta.descripcion', read_only=True)
    usuario_nombre=CharField(source='usuario.username', read_only=True)
    detallesmc = DetalleMovimientoCuentaSerializer(many=True)
    class Meta:
        model = MovimientoCuenta
        fields = ['presupuesto','presupuesto_descripcion', 'gerencia','gerencia_descripcion', 'cuenta','cuenta_descripcion','usuario','usuario_nombre', 'detallesmc']