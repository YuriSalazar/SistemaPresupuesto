from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction
from .serializers import MovimientoCuentaSerializer
from .models import Presupuesto, Gerencia, Cuenta, User, Mes, DetalleMovimientoCuenta, MovimientoCuenta
from drf_yasg.utils import swagger_auto_schema
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from ...permissions import CustomPermission
from config.utils.Pagination import PaginationMixin
import logging.handlers

# Configura el logger
logger = logging.getLogger(__name__)

# Create your views here.

"""
EndPoint de MovimientoCuenta
"""

class MovimientoCuentaAPIView(PaginationMixin, APIView):
    """
    Vista para listar todos los movimientos de las cuentas o crear nuevos movimientos en las cuentas.
    """
    permission_classes = [IsAuthenticated, CustomPermission]
    model = MovimientoCuenta

    @swagger_auto_schema(responses={200: MovimientoCuentaSerializer(many=True)})
    def get(self,request):
        """
        Listar todos los movimientos en las cuentas.
        """
        logger.info("GET request to list all movimientos de las cuentas")
        movimientoc = MovimientoCuenta.objects.filter(estado=1).prefetch_related('detallesmc').order_by('id')
        page = self.paginate_queryset(movimientoc, request)

        if page is not None:
            serializer = MovimientoCuentaSerializer(page, many=True)
            logger.info("Paginated response for movimientos de las cuenta")
            return self.get_paginated_response(serializer.data)

        serializer = MovimientoCuentaSerializer(movimientoc, many=True)
        logger.error("Returning all movimientos de cuenta without pagination")
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(request_body=MovimientoCuentaSerializer, responses={201: MovimientoCuentaSerializer()})
    def post(self, request):
        serializer = MovimientoCuentaSerializer(data=request.data)
        if serializer.is_valid():
            try:
                with transaction.atomic():
                    presupuesto=get_object_or_404(Presupuesto, id=serializer.validated_data.get('presupuesto').id)
                    gerencia=get_object_or_404(Gerencia, id=serializer.validated_data.get('gerencia').id)
                    cuenta=get_object_or_404(Cuenta, id=serializer.validated_data.get('cuenta').id)
                    usuario=get_object_or_404(User, id=serializer.validated_data.get('usuario').id)
                    detalle_data=serializer.validated_data.get('detallesmc')
                    movimientocuenta=MovimientoCuenta.objects.create(presupuesto=presupuesto,gerencia=gerencia,cuenta=cuenta,usuario=usuario)
                    total=0

                    for detalle in detalle_data:
                        mes=get_object_or_404(Mes, id=detalle['mes'].id)
                        concepto=detalle['concepto']
                        monto=detalle['monto']

                        total+=monto

                        DetalleMovimientoCuenta.objects.create(
                            movimientocuenta=movimientocuenta,
                            mes=mes,
                            concepto=concepto,
                            monto=monto,
                        )
                    movimientocuenta.save()
                    movimientocuenta_serializer=MovimientoCuentaSerializer(movimientocuenta)
                    return Response(movimientocuenta_serializer.data, status=status.HTTP_201_CREATED)

            except Exception as e:
                Response({"Error":str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class MovimientoCuentaDetails(APIView):
    """
    Vista para obtener, actualizar o eliminar un movimiento de cuenta especifico.
    """
    permission_classes = [IsAuthenticated, CustomPermission]
    model = MovimientoCuenta

    @swagger_auto_schema(responses={204: 'No Content'})
    def delete(self,request,pk):
        """
        Eliminar un movimiento de cuenta por su ID.
        """
        logger.info("DELETE request to delete movimientos de cuentas with ID: %s", pk)
        movimientoc=get_object_or_404(MovimientoCuenta, id=pk, estado=1)
        if not movimientoc:
            return Response({'Error':'Movimientos de cuenta no encontrados'}, status=status.HTTP_404_NOT_FOUND)

        self.check_object_permissions(request,movimientoc)
        movimientoc.estado=0 # Marcar como eliminado
        movimientoc.save()
        # Marcar detalles como eliminados
        DetalleMovimientoCuenta.objects.filter(movimientocuenta=movimientoc).update(estado=0)
        logger.info("Movimientos de Cuentas deleted successfully with ID: %s", pk)
        return Response(status=status.HTTP_204_NO_CONTENT)
