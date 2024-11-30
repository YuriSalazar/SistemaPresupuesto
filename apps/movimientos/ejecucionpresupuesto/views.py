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
from django.db import connection # Para llamar procedimiento almacenado

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

class EjecucionPresupuestoDetails(APIView):
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

class EjecucionPresupuestoReporte(PaginationMixin, APIView):
    """
    Vista para listar todos las ejecuciones presupuestarias.
    """
    permission_classes = [IsAuthenticated, CustomPermission]
    model = EjecucionPresupuesto

    @swagger_auto_schema(responses={200: EjecucionPresupuestoSerializer(many=True)})
    def get(self, request):
        """
        Listar todos las ejecuciones del presupuesto con su detalle ejecutando un procedimiento almacenado y devolviendo JSON directamente.
        """
        try:
            # Llama al procedimiento almacenado usando cursor.execute
            with connection.cursor() as cursor:
                # Ejecuta el procedimiento almacenado
                cursor.execute("EXEC usp_GetEjecucionPresupuestoConDetalles")

                # Obtén los nombres de las columnas
                columns = [col[0] for col in cursor.description]

                # Obtén los datos y mapea con los nombres de las columnas
                results = [dict(zip(columns, row)) for row in cursor.fetchall()]

                # Construye manualmente el JSON

                ejecucionpresupuesto_json = [
                   {
                       "presupuesto": item["presupuesto"],
                       "gerencia": item["gerencia"],
                       "cuenta": item["cuenta"],
                       "usuario": item["usuario"],
                       "mes": item["mes"],
                       "justificacion": item["justificacion"],
                       "montoreal": item["montoreal"]
                   }
                   for item in results
                ]

            # Serializa los datos
            logger.info("Stored procedure executed successfully")
            return Response(ejecucionpresupuesto_json, status=200)

        except Exception as e:
            logger.error(f"Error executing stored procedure: {str(e)}")
            return Response({"Error": str(e)}, status=500)

class EjecucionPresupuestoDetailsReporte(APIView):
    """
    Vista para obtener los detalles de la ejecucion de un presupuesto específico junto con sus detalles (maestro-detalle).
    """
    permission_classes = [IsAuthenticated, CustomPermission]
    model = EjecucionPresupuesto

    def get(self, request, ejecucionpresupuesto_id):
        logger.info(f"GET request to get ejecucion presupuesto details with id={ejecucionpresupuesto_id}")
        try:
            with connection.cursor() as cursor:
                # Ejecuta el procedimiento almacenado con un parámetro
                cursor.execute("EXEC usp_GetEjecucionPresupuestoEspecifico @ejecucionpresupuestoID = %s", [ejecucionpresupuesto_id])

                # Primer conjunto de resultados: Información general del movimiento de cuenta
                ejecucionpresupuesto_row = cursor.fetchone()
                if not ejecucionpresupuesto_row:
                    logger.error(f"No data found for ejecucion presupuesto ID={ejecucionpresupuesto_id}")
                    return Response({"error": "Ejecucion de presupuesto no encontrado"}, status=404)

                # Obtén los nombres de las columnas del primer conjunto
                ejecucionpresupuesto_columns = [col[0] for col in cursor.description]
                ejecucionpresupuesto_info = dict(zip(ejecucionpresupuesto_columns, ejecucionpresupuesto_row))

                # Cambiar al segundo conjunto de resultados: Detalles del movimiento
                cursor.nextset()
                detalle_columns = [col[0] for col in cursor.description]
                detalles = [dict(zip(detalle_columns, row)) for row in cursor.fetchall()]

                # Construir el JSON final
                ejecucionpresupuesto_info["detalles"] = detalles

            logger.info("Stored procedure executed successfully for ejecucion presupuesto details")
            return Response(ejecucionpresupuesto_info, status=200)

        except Exception as e:
            logger.error(f"Error executing stored procedure: {str(e)}", exc_info=True)
            return Response({"error": "Error ejecutando el procedimiento almacenado"}, status=500)




