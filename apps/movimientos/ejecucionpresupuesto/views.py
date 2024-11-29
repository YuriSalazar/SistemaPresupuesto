from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction
from .serializers import EjecucionPresupuestoSerializer
from .models import Presupuesto, Gerencia, Cuenta, User, Mes, DetalleEjecucionPresupuesto, EjecucionPresupuesto
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
EndPoint de EjecucionPresupuesto
"""
class EjecucionPresupuestoAPIView(PaginationMixin, APIView):
    """
    Vista para listar todos las ejecuciones presupuestarias o crear nuevas ejecuciones en las cuentas.
    """
    permission_classes = [IsAuthenticated, CustomPermission]
    model = EjecucionPresupuesto

    @swagger_auto_schema(responses={200: EjecucionPresupuestoSerializer(many=True)})
    def get(self, request):
        """
        Listar las ejecuciones del presupuesto
        """
        logger.info("GET request to list all ejecucion del presupuesto")
        ejecucionp=EjecucionPresupuesto.objects.filter(estado=1).prefetch_related('detallesep').order_by('id')
        page = self.paginate_queryset(ejecucionp, request)

        if page is not None:
            serializer = EjecucionPresupuestoSerializer(page, many=True)
            logger.info("Paginated response for ejecucion presupuesto")
            return self.get_paginated_response(serializer.data)

        serializer = EjecucionPresupuestoSerializer(ejecucionp, many=True)
        logger.error("Returning all ejecucion presupuesto without pagination")
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(request_body=EjecucionPresupuestoSerializer, responses={201: EjecucionPresupuestoSerializer()})
    def post(self, request):
        serializer = EjecucionPresupuestoSerializer(data=request.data)
        if serializer.is_valid():
            try:
                with transaction.atomic():
                    presupuesto = get_object_or_404(Presupuesto, id=serializer.validated_data.get('presupuesto').id)
                    gerencia = get_object_or_404(Gerencia, id=serializer.validated_data.get('gerencia').id)
                    cuenta = get_object_or_404(Cuenta, id=serializer.validated_data.get('cuenta').id)
                    usuario = get_object_or_404(User, id=serializer.validated_data.get('usuario').id)
                    detalle_data=serializer.validated_data.get('detallesep')
                    ejecucionpresupuesto = EjecucionPresupuesto.objects.create(presupuesto=presupuesto,gerencia=gerencia,cuenta=cuenta,usuario=usuario)
                    total=0

                    for detalle in detalle_data:
                        mes=get_object_or_404(Mes, id=detalle['mes'].id)
                        montoreal=detalle['montoreal']
                        justificacion=detalle['justificacion']

                        total+=montoreal

                        DetalleEjecucionPresupuesto.objects.create(
                            ejecucionpresupuesto=ejecucionpresupuesto,
                            mes=mes,
                            montoreal=montoreal,
                            justificacion=justificacion,
                        )
                    ejecucionpresupuesto.save()
                    ejecucionpresupuesto_serializer=EjecucionPresupuestoSerializer(ejecucionpresupuesto)
                    return Response(ejecucionpresupuesto_serializer.data, status=status.HTTP_201_CREATED)

            except Exception as e:
                return Response({"Error":str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class EjeccionPresupuestoDetails(APIView):
    """
    Vista para obtener, actualizar o eliminar una ejecucion del presupuesto especifica.
    """
    permission_classes = [IsAuthenticated, CustomPermission]
    model = EjecucionPresupuesto

    @swagger_auto_schema(responses={204: 'No Content'})
    def delete(self, request, pk):
        """
        Eliminar una ejecucion del presupuesto por su ID.
        """
        logger.info("DELETE request to delete ejecucion del prespuesto with ID: %s", pk)
        ejecucionp=get_object_or_404(EjecucionPresupuesto, id=pk, estado=1)
        if not ejecucionp:
            return Response({'Error':'Ejecucion de prespuesto no encontrados'}, status=status.HTTP_404_NOT_FOUND)
        self.check_object_permissions(request, ejecucionp)
        ejecucionp.estado=0 # Marcar como eliminado
        ejecucionp.save()
        # Marcar detalles como eliminados
        DetalleEjecucionPresupuesto.objects.filter(ejecucionpresupuesto=ejecucionp).update(estado=0)
        logger.info("Ejecucion de presupuesto deleted successfully with ID: %s", pk)
        return Response(status=status.HTTP_204_NO_CONTENT)





