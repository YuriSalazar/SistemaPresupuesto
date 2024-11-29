from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import TipoMovimiento
from .serializers import TipoMovimientoSerializer
from drf_yasg.utils import swagger_auto_schema
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from ...permissions import CustomPermission
from config.utils.Pagination import PaginationMixin
import logging.handlers

# Configura el logger
logger = logging.getLogger(__name__)

# Create your views here.
class TipoMovimientoApiView(PaginationMixin, APIView):
    """
    Vista para listar todos los Tipos de Movimientos o crear un nuevo Tipo de Movimiento
    """
    permission_classes = [IsAuthenticated, CustomPermission]
    model = TipoMovimiento
    @swagger_auto_schema(responses={200: TipoMovimientoSerializer(many=True)})
    def get(self, request):
        """
        Listar todos los Tipos de Movimientos.
        """
        logger.info("GET request to list all Tipo Movimientos")
        tipomovimiento = TipoMovimiento.objects.all().order_by('id')
        page = self.paginate_queryset(tipomovimiento, request)

        if page is not None:
            serializer = TipoMovimientoSerializer(page, many=True)
            logger.info("Paginated response for Tipo Movimientos")
            return self.get_paginated_response(serializer.data)

        serializer = TipoMovimientoSerializer(tipomovimiento, many=True)
        logger.error("Returning all departamentos without pagination")
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(request_body=TipoMovimientoSerializer, responses={201: TipoMovimientoSerializer()})
    def post(self, request):
        """
        Crear un nuevo Tipo de Movimiento.
        """
        logger.info("POST request to create a new tipo movimiento")
        serializer = TipoMovimientoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            logger.info("Tipo Movimiento created successfully")
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        logger.error("Failed to create tipo movimiento: %s", serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TipoMovimientoDetails(APIView):
    """
    Vista para obtener, actualizar o eliminar un Tipo de Movimiento especifico.
    """
    @swagger_auto_schema(responses={200: TipoMovimientoSerializer()})
    def get(self, request, pk):
        """
        Obtener un Tipo de movimiento especifico por su ID.
        """
        logger.info("GET request to obtain tipo movimiento with ID: %s", pk)
        tipomovimiento = get_object_or_404(TipoMovimiento, id=pk)
        if not tipomovimiento:
            return Response({'Error':'Tipo de Movimiento no encontrado.'},status=status.HTTP_404_NOT_FOUND)
        serializer = TipoMovimientoSerializer(tipomovimiento)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(request_body=TipoMovimientoSerializer, responses={200: TipoMovimientoSerializer()})
    def put(self, request, pk):
        """
        Actualizar completamente un Tipo de Movimiento por su ID.
        """
        logger.info("PUT request to update tipo movimiento with ID: %s", pk)
        tipomovimiento = get_object_or_404(TipoMovimiento, id=pk)
        if not tipomovimiento:
            return Response({'Error':'Tipo de Movimiento no encontrado.'},status=status.HTTP_404_NOT_FOUND)
        self.check_object_permissions(request, tipomovimiento)
        serializer = TipoMovimientoSerializer(tipomovimiento, data=request.data)
        if serializer.is_valid():
            serializer.save()
            logger.info("Tipo Movimiento updated successfully with ID: %s", pk)
            return Response(serializer.data)
        logger.error("Failed to update tipo movimiento with ID: %s. Errors: %s", pk, serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(request_body=TipoMovimientoSerializer, responses={200: TipoMovimientoSerializer()})
    def patch(self, request, pk):
        """
        Actualizar parcialmente un Tipo de Movimiento por su ID.
        """
        logger.info("PATCH request to partially update tipo movimiento with ID: %s", pk)
        tipomovimiento = get_object_or_404(TipoMovimiento, id=pk)
        if not tipomovimiento:
            return Response({'Error':'Tipo de Movimiento no encontrado.'},status=status.HTTP_404_NOT_FOUND)
        self.check_object_permissions(request, tipomovimiento)
        serializer = TipoMovimientoSerializer(tipomovimiento, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            logger.info("Tipo Movimiento partially updated successfully with ID: %s", pk)
            return Response(serializer.data)
        logger.error("Failed to partially update tipo movimiento with ID: %s. Errors: %s", pk, serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(responses={204: 'No Content'})
    def delete(self, request, pk):
        """
        Eliminar un Tipo de Movimiento por su ID.
        """
        logger.info("DELETE request to delete tipo movimiento with ID: %s", pk)
        tipomovimiento= get_object_or_404(TipoMovimiento, id=pk)
        if not tipomovimiento:
            return Response({'Error':'Tipo de Movimiento no encontrado.'},status=status.HTTP_404_NOT_FOUND)
        self.check_object_permissions(request, tipomovimiento)
        tipomovimiento.delete()
        logger.info("Tipo Movimiento deleted successfully with ID: %s", pk)
        return Response(status=status.HTTP_204_NO_CONTENT)

