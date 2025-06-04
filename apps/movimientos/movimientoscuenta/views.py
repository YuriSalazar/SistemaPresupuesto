from http.client import responses
from django.shortcuts import get_object_or_404
from django.db.models import Sum, Avg, Max
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
from django.db import connection # Para llamar procedimiento almacenado

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
    #permission_classes = [IsAuthenticated, CustomPermission]
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
    #permission_classes = [IsAuthenticated, CustomPermission]
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

class MovimientoCuentaReporte(PaginationMixin, APIView):
    """
    Vista para listar todos los movimientos de las cuentas.
    """
    #permission_classes = [IsAuthenticated, CustomPermission]
    model = MovimientoCuenta

    @swagger_auto_schema(responses={200: MovimientoCuentaSerializer(many=True)})
    def get(self, request):
        """
        Listar todos los movimientos de las cuentas con su detalle ejecutando un procedimiento almacenado y devolviendo JSON directamente.
        """
        try:
            # Llama al procedimiento almacenado usando cursor.execute
            with connection.cursor() as cursor:
                # Ejecuta el procedimiento almacenado
                cursor.execute("EXEC usp_GetMovimientosCuentaConDetalles")

                # Obtén los nombres de las columnas
                columns = [col[0] for col in cursor.description]

                # Obtén los datos y mapea con los nombres de las columnas
                results = [dict(zip(columns, row)) for row in cursor.fetchall()]

                # Construye manualmente el JSON

                movimientocuenta_json = [
                   {
                       "presupuesto": item["presupuesto"],
                       "gerencia": item["gerencia"],
                       "cuenta": item["cuenta"],
                       "usuario": item["usuario"],
                       "mes": item["mes"],
                       "concepto": item["concepto"],
                       "monto": item["monto"]
                   }
                   for item in results
                ]

            # Serializa los datos
            logger.info("Stored procedure executed successfully")
            return Response(movimientocuenta_json, status=200)

        except Exception as e:
            logger.error(f"Error executing stored procedure: {str(e)}")
            return Response({"Error": str(e)}, status=500)


class MovimientoCuentaDetailsReporte(APIView):
    """
    Vista para obtener los detalles de un movimiento de cuenta específico junto con sus detalles (maestro-detalle).
    """
    #permission_classes = [IsAuthenticated, CustomPermission]
    model = MovimientoCuenta

    def get(self, request, movimientocuenta_id):
        logger.info(f"GET request to get movimiento cuenta details with id={movimientocuenta_id}")
        try:
            with connection.cursor() as cursor:
                # Ejecuta el procedimiento almacenado con un parámetro
                cursor.execute("EXEC usp_GetMovimientoCuentaEspecifica @movimientocuentaID = %s", [movimientocuenta_id])

                # Primer conjunto de resultados: Información general del movimiento de cuenta
                movimientocuenta_row = cursor.fetchone()
                if not movimientocuenta_row:
                    logger.error(f"No data found for movimiento cuenta ID={movimientocuenta_id}")
                    return Response({"error": "Movimiento de cuenta no encontrado"}, status=404)

                # Obtén los nombres de las columnas del primer conjunto
                movimientocuenta_columns = [col[0] for col in cursor.description]
                movimientocuenta_info = dict(zip(movimientocuenta_columns, movimientocuenta_row))

                # Cambiar al segundo conjunto de resultados: Detalles del movimiento
                cursor.nextset()
                detalle_columns = [col[0] for col in cursor.description]
                detalles = [dict(zip(detalle_columns, row)) for row in cursor.fetchall()]

                # Construir el JSON final
                movimientocuenta_info["detalles"] = detalles

            logger.info("Stored procedure executed successfully for movimiento cuenta details")
            return Response(movimientocuenta_info, status=200)

        except Exception as e:
            logger.error(f"Error executing stored procedure: {str(e)}", exc_info=True)
            return Response({"error": "Error ejecutando el procedimiento almacenado"}, status=500)


class ReporteGastosTotales(APIView):
    """
    Vista para listar los gastos totales por mes y por cuenta.
    """
    #permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            # Consulta y agrupación
            datos = (
                DetalleMovimientoCuenta.objects.filter(
                    estado=1,  # Detalles activos
                    movimientocuenta__estado=1  # Movimientos activos
                )
                .values(
                    'mes__id',
                    'mes__descripcion',
                    'movimientocuenta__cuenta__numeroCuenta',
                    'movimientocuenta__cuenta__descripcion'
                )
                .annotate(total_gasto=Sum('monto'))
                .order_by('mes__id')
            )

            # Eliminar 'movimientocuenta__gerencia__id' de la salida final
            resultado = [
                {
                    "mes_descripcion": item["mes__descripcion"],
                    "numero_cuenta": item["movimientocuenta__cuenta__numeroCuenta"],
                    "cuenta_descripcion": item["movimientocuenta__cuenta__descripcion"],
                    "total_gasto": item["total_gasto"]
                }
                for item in datos
            ]

            # Retorno de los datos
            return Response(resultado, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"Error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ReporteGastosPorGerencia(APIView):
    """
    Vista para listar los gastos totales por gerencia.
    """
    #permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            # Consulta y agrupación por gerencia
            datos = (
                DetalleMovimientoCuenta.objects.filter(
                    estado=1,  # Detalles activos
                    movimientocuenta__estado=1,  # Movimientos activos
                    movimientocuenta__gerencia__estado=1  # Gerencias activas
                )
                .values(
                    'movimientocuenta__gerencia__id',  # Usado solo para ordenar
                    'movimientocuenta__gerencia__descripcion'
                )
                .annotate(total_gasto=Sum('monto'))
                .order_by('movimientocuenta__gerencia__id')
            )

            # Eliminar 'movimientocuenta__gerencia__id' de la salida final
            resultado = [
                {
                    "gerencia_descripcion": item["movimientocuenta__gerencia__descripcion"],
                    "total_gasto": item["total_gasto"]
                }
                for item in datos
            ]

            # Retorno de los datos
            return Response(resultado, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"Error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class ReporteGastosPromedioGerencia(APIView):
    """
    Vista para listar los gastos totales por gerencia.
    """
    #permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            # Consulta y agrupación por gerencia
            datos = (
                DetalleMovimientoCuenta.objects.filter(
                    estado=1,  # Detalles activos
                    movimientocuenta__estado=1,  # Movimientos activos
                    movimientocuenta__gerencia__estado=1  # Gerencias activas
                )
                .values(
                    'movimientocuenta__gerencia__id',  # Usado solo para ordenar
                    'movimientocuenta__gerencia__descripcion'
                )
                .annotate(gasto_promedio=Avg('monto'))
                .order_by('movimientocuenta__gerencia__id')
            )

            # Eliminar 'movimientocuenta__gerencia__id' de la salida final
            resultado = [
                {
                    "gerencia_descripcion": item["movimientocuenta__gerencia__descripcion"],
                    "gasto_promedio": item["gasto_promedio"]
                }
                for item in datos
            ]

            # Retorno de los datos
            return Response(resultado, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"Error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class GastoTotalPorMes(APIView):
    """
    Vista para listar los gastos totales por mes.
    """
    #permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            # Consulta y agrupación
            datos = (
                DetalleMovimientoCuenta.objects.filter(
                    estado=1,  # Detalles activos
                    movimientocuenta__estado=1  # Movimientos activos
                )
                .values(
                    'mes__id',
                    'mes__descripcion'
                )
                .annotate(total_gasto_del_mes=Sum('monto'))
                .order_by('mes__id')
            )

            # Eliminar 'movimientocuenta__gerencia__id' de la salida final
            resultado = [
                {
                    "mes_descripcion": item["mes__descripcion"],
                    "total_gasto_del_mes": item["total_gasto_del_mes"]
                }
                for item in datos
            ]

            # Retorno de los datos
            return Response(resultado, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"Error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class TresMayoresGastosPorGerencia(APIView):
    """
    Vista para calculas los tres gastos mas altos por gerencia.
    """
    #permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            # Consulta y agrupación por gerencia
            datos = (
                DetalleMovimientoCuenta.objects.filter(
                    estado=1,  # Detalles activos
                    movimientocuenta__estado=1,  # Movimientos activos
                    movimientocuenta__gerencia__estado=1  # Gerencias activas
                )
                .values(
                    'movimientocuenta__gerencia__descripcion'
                )
                .annotate(gasto_maximo=Max('monto'))
                .order_by('-gasto_maximo')
            )

            # Eliminar 'movimientocuenta__gerencia__id' de la salida final
            resultado = [
                {
                    "gerencia_descripcion": item["movimientocuenta__gerencia__descripcion"],
                    "gasto_maximo": item["gasto_maximo"]
                }
                for item in datos
            ]

            # Retorno de los datos
            return Response(resultado[:3], status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"Error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)