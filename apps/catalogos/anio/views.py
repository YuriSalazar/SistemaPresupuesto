from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Anio
from .serializers import AnioSerializer
from drf_yasg.utils import swagger_auto_schema
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated # Para proteger la vista

#from .. import anio
from ...permissions import CustomPermission
from config.utils.Pagination import PaginationMixin
import logging.handlers

# Configura el logger
logger = logging.getLogger(__name__)

# Create your views here.
class AnioApiView(PaginationMixin, APIView):
    """
    Vista para listar todos los anios o crear un nuevo anio
    """
    #permission_classes = [IsAuthenticated, CustomPermission] # Para proteger la vista
    model = Anio # Definiendo el modelo explicitamente

    @swagger_auto_schema(responses={200: AnioSerializer(many=True)})
    def get(self, request):
        """
        Listar todos los anios.
        """
        logger.info(f"GET request to list all anios")
        anio = Anio.objects.order_by('id')
        page = self.paginate_queryset(anio,request)

        if page is not None:
            serializer = AnioSerializer(page, many=True)
            logger.info("Paginated response for anios.")
            return self.get_paginated_response(serializer.data)

        serializer = AnioSerializer(anio, many=True)
        logger.error("Returning all anios without pagination.")
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(request_body=AnioSerializer, responses={201: AnioSerializer()})
    def post(self, request):
        """
        Crear un nuevo anio.
        """
        logger.info("POST request to create a new anio.")

        serializer = AnioSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            logger.info("Anio created successfully")
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        logger.error("Failed to create anio: %s", serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AnioDetails(APIView):
    """
    Vista para obtener, actualizar o eliminar un anio especifico.
    """
    #permission_classes =[IsAuthenticated, CustomPermission]
    model = Anio
    @swagger_auto_schema(responses={200: AnioSerializer()})
    def get(self, request, pk):
        """
        Obtener un anio especifico por su ID.
        """
        logger.info("GET request to obtain anio with ID: %s", pk)
        anio = get_object_or_404(Anio, id=pk)
        if not anio:
            return Response({'Error':'Anio no encontrado.'},status=status.HTTP_404_NOT_FOUND)
        serializer = AnioSerializer(anio)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(request_body=AnioSerializer, responses={200: AnioSerializer()})
    def put(self, request, pk):
        """
        Actualizar completamente un anio por su ID.
        """
        logger.info("PUT request to update an anio with ID: %s.", pk)
        anio =get_object_or_404(Anio, id=pk)
        if not anio:
            return Response({'Error':'Anio no encontrado.'},status=status.HTTP_404_NOT_FOUND)
        self.check_object_permissions(request, anio)
        serializer = AnioSerializer(anio, data=request.data)
        if serializer.is_valid():
            serializer.save()
            logger.info("Anio updated successfully with ID: %s.", pk)
            return Response(serializer.data)
        logger.error("Failed to update anio with ID: %s. Errors:%s", pk, serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(request_body=AnioSerializer, responses={200: AnioSerializer()})
    def patch(self, request, pk):
        """
        Actualizar parcialmente un anio por su ID.
        """
        logger.info("PATCH request to partially update an anio with ID: %s.", pk)
        anio =get_object_or_404(Anio, id=pk)
        if not anio:
            return Response({'Error':'Anio no encontrado.'},status=status.HTTP_404_NOT_FOUND)
        self.check_object_permissions(request, anio)
        serializer = AnioSerializer(anio, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            logger.info("Anio partially updated successfully with ID: %s.", pk)
            return Response(serializer.data)
        logger.error("Failed to partially update anio with ID: %s. Errors:%s", pk, serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(responses={204: 'No Content'})
    def delete(self, request, pk):
        """
        Eliminar un anio por su ID.
        """
        logger.info("DELETE request to delete an anio with ID: %s.", pk)
        anio = get_object_or_404(Anio, id=pk)
        if not anio:
            return Response({'Error':'Anio no encontrado.'},status=status.HTTP_404_NOT_FOUND)
        self.check_object_permissions(request, anio)
        anio.delete()
        logger.info("Anio deleted successfully with ID: %s.", pk)
        return Response(status=status.HTTP_204_NO_CONTENT)

class AnioCantidad(APIView):
    #permission_classes = [IsAuthenticated]  # Mantén los permisos necesarios

    def get(self, request):
        # Lógica para contar los registros en el modelo
        cantidad_anios = Anio.objects.count()
        return Response({'cantidad_anios': cantidad_anios}, status=status.HTTP_200_OK)



