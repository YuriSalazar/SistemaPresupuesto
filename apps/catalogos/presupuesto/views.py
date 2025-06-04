from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Presupuesto
from .serializers import PresupuestoSerializer
from drf_yasg.utils import swagger_auto_schema
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from ...permissions import CustomPermission
from config.utils.Pagination import PaginationMixin
import logging.handlers

# Configura el logger
logger = logging.getLogger(__name__)

# Create your views here.
class PresupuestoApiView(PaginationMixin, APIView):
    """
    Vista para listar todos los presupuestos o crear un nuevo prespuesto
    """
    permission_classes = [IsAuthenticated, CustomPermission]
    model = Presupuesto

    @swagger_auto_schema(responses={200: PresupuestoSerializer(many=True)})
    def get(self, request):
        """
        Listar todos los presupuestos.
        """
        logger.info("GET request to list all presupuestos")
        presupuesto = Presupuesto.objects.filter(estado=1).order_by('id')
        page = self.paginate_queryset(presupuesto, request)

        if page is not None:
            serializer = PresupuestoSerializer(page, many=True)
            logger.info("Paginated response for presupuestos")
            return self.get_paginated_response(serializer.data)

        serializer = PresupuestoSerializer(presupuesto, many=True)
        logger.error("Returning all presupuestos without pagination")
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(request_body=PresupuestoSerializer, responses={201: PresupuestoSerializer()})
    def post(self, request):
        """
        Crear un nuevo presupuesto.
        """
        logger.info("POST request to create a new presupuesto")
        serializer = PresupuestoSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            logger.info("Presupuesto created successfully")
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        logger.error("Failed to create presupuesto: %s", serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PresupuestoDetails(APIView):
    """
    Vista para obtener, actualizar o eliminar un presupuesto especifico.
    """
    permission_classes = [IsAuthenticated, CustomPermission]
    model = Presupuesto
    @swagger_auto_schema(responses={200: PresupuestoSerializer()})
    def get(self, request, pk):
        """
        Obtener un presupuesto especifico por su ID.
        """
        logger.info("GET request to obtain presupuesto with ID: %s", pk)
        presupuesto = get_object_or_404(Presupuesto, id=pk, estado=1)

        if not presupuesto:
            return Response({'Error':'Presupuesto no encontrado.'},status=status.HTTP_404_NOT_FOUND)
        serializer = PresupuestoSerializer(presupuesto)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(request_body=PresupuestoSerializer, responses={200: PresupuestoSerializer()})
    def put(self, request, pk):
        """
        Actualizar completamente un prespuesto por su ID.
        """
        logger.info("PUT request to update presupuesto with ID: %s", pk)
        presupuesto = get_object_or_404(Presupuesto, id=pk, estado=1)
        if not presupuesto:
            return Response({'Error':'Presupuesto no encontrado.'},status=status.HTTP_404_NOT_FOUND)
        self.check_object_permissions(request, presupuesto)
        serializer = PresupuestoSerializer(presupuesto, data=request.data)
        if serializer.is_valid():
            serializer.save()
            logger.info("Presupuesto updated successfully with ID: %s", pk)
            return Response(serializer.data)
        logger.error("Failed to update presupuesto with ID: %s. Errors: %s", pk, serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(request_body=PresupuestoSerializer, responses={200: PresupuestoSerializer()})
    def patch(self, request, pk):
        """
        Actualizar parcialmente un presupuesto por su ID.
        """
        logger.info("PATCH request to partially update presupuesto with ID: %s", pk)
        presupuesto = get_object_or_404(Presupuesto, id=pk, estado=1)
        if not presupuesto:
            return Response({'Error':'Presupuesto no encontrado.'},status=status.HTTP_404_NOT_FOUND)
        self.check_object_permissions(request, presupuesto)
        serializer = PresupuestoSerializer(presupuesto, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            logger.info("Presupuesto partially updated successfully with ID: %s", pk)
            return Response(serializer.data)
        logger.error("Failed to partially update presupuesto with ID: %s. Errors: %s", pk, serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(responses={204: 'No Content'})
    def delete(self, request, pk):
        """
        Eliminar un presupuesto por su ID.
        """
        logger.info("DELETE request to delete presupuesto with ID: %s", pk)
        presupuesto = get_object_or_404(Presupuesto, id=pk, estado=1)
        if not presupuesto:
            return Response({'Error':'Presupuesto no encontrado.'},status=status.HTTP_404_NOT_FOUND)
        self.check_object_permissions(request, presupuesto)
        presupuesto.estado = 0
        presupuesto.save()
        logger.info("Presupuesto deleted successfully with ID: %s", pk)
        return Response(status=status.HTTP_204_NO_CONTENT)

class PresupuestoCantidad(APIView):
    permission_classes = [IsAuthenticated]  # Mantén los permisos necesarios

    def get(self, request):
        # Lógica para contar los presupuestos grabados
        cantidad_presupuestos = Presupuesto.objects.count()
        return Response({'cantidad_Presupuestos': cantidad_presupuestos}, status=status.HTTP_200_OK)
