from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Gerencia
from .serializers import GerenciaSerializer
from drf_yasg.utils import swagger_auto_schema
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from ...permissions import CustomPermission
from config.utils.Pagination import PaginationMixin
import logging.handlers

# Configarar el logger
logger = logging.getLogger(__name__)

# Create your views here.
class GerenciaApiView(PaginationMixin, APIView):
    """
    Vista para listar todas las gerencias o crear una nueva gerencia
    """
    permission_classes = [IsAuthenticated, CustomPermission]
    model=Gerencia

    @swagger_auto_schema(responses={200: GerenciaSerializer(many=True)})
    def get(self, request):
        """
        Listar todas las gerencias
        """
        logger.info("GET request to list all gerencias")
        gerencia = Gerencia.objects.filter(estado=1).order_by('id')
        page = self.paginate_queryset(gerencia,request)

        if page is not None:
            serializer = GerenciaSerializer(gerencia, many=True)
            logger.info("Paginated response for gerencia")
            return self.get_paginated_response(serializer.data)
        serializer = GerenciaSerializer(gerencia, many=True)
        logger.info("Returning all gerencia without pagination")
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(request_body=GerenciaSerializer, responses={201: GerenciaSerializer()})
    def post(self, request):
        """
        Crear una nueva gerencia.
        """
        logger.info("POST request to create a new gerencia")

        serializer = GerenciaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            logger.info("Gerencia created successfully")
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        logger.error("Failed to create gerencia: %s", serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class GerenciaDetails(APIView):
    """
    Vista para obtener, actualizar o eliminar una gerencia especifica.
    """

    permission_classes = [IsAuthenticated, CustomPermission]
    model=Gerencia

    @swagger_auto_schema(responses={200: GerenciaSerializer()})
    def get(self, request, pk):
        """
        Obtener una gerencia especifica por su ID.
        """
        logger.info("GET request to obtain gerencia with pk: %s", pk)
        gerencia = get_object_or_404(Gerencia, id=pk, estado=1)
        if not gerencia:
            return Response({'Error': 'Gerencia no encontrada'}, status=status.HTTP_404_NOT_FOUND)
        serializer = GerenciaSerializer(gerencia)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(request_body=GerenciaSerializer, responses={200: GerenciaSerializer()})
    def put(self, request, pk):
        """
        Actualizar completamente una gerencia por su ID.
        """
        logger.info("PUT request to update gerencia with pk: %s", pk)
        gerencia = get_object_or_404(Gerencia, id=pk, estado=1)

        if not gerencia:
            return Response({'Error': 'Gerencia no encontrada'}, status=status.HTTP_404_NOT_FOUND)
        self.check_object_permissions(request, gerencia)
        serializer = GerenciaSerializer(gerencia, data=request.data)
        if serializer.is_valid():
            serializer.save()
            logger.info("Gerencia updated successfully with ID: %s", pk)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        logger.error("Failed to update gerencia with ID: %s", pk)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(request_body=GerenciaSerializer, responses={200: GerenciaSerializer()})
    def patch(self, request, pk):
        """
        Actualizar parcialmente una gerencia por su ID.
        """
        logger.info("PATCH request to partially update gerencia with pk: %s", pk)
        gerencia = get_object_or_404(Gerencia, id=pk, estado=1)
        if not gerencia:
            return Response({'Error': 'Gerencia no encontrada'}, status=status.HTTP_404_NOT_FOUND)
        self.check_object_permissions(request, gerencia)
        serializer = GerenciaSerializer(gerencia, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            logger.info("Gerencia partially updated successfully with ID: %s", pk)
            return Response(serializer.data, status=status.HTTP_200_OK)
        logger.error("Failed to partially update gerencia with ID: %s", pk)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(responses={204: 'No Content'})
    def delete(self, request, pk):
        """
        Eliminar una gerencia por su ID.
        """
        logger.info("DELETE request to delete gerencia with pk: %s", pk)
        gerencia = get_object_or_404(Gerencia, id=pk, estado=1)
        if not gerencia:
            return Response({'Error': 'Gerencia no encontrada'}, status=status.HTTP_404_NOT_FOUND)
        self.check_object_permissions(request, gerencia)
        gerencia.estado = 0
        gerencia.save()
        logger.info("Gerencia deleted successfully with ID: %s", pk)
        return Response(status=status.HTTP_204_NO_CONTENT)