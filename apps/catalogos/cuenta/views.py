from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status
from .models import Cuenta
from .serializers import CuentaSerializer
from drf_yasg.utils import swagger_auto_schema
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from ...permissions import CustomPermission
from config.utils.Pagination import PaginationMixin
import logging.handlers

# Configurar el logger
logger = logging.getLogger(__name__)

# Create your views here.
class CuentaApiView(PaginationMixin, APIView):
    """
    Vista para listar todas las cuentas o crear una nueva cuenta
    """
    permission_classes = [IsAuthenticated, CustomPermission]
    model = Cuenta

    @swagger_auto_schema(responses={200: CuentaSerializer(many=True)})
    def get(self, request):
        """
        Listar todas las cuentas
        """
        logger.info("GET request to list all cuentas")
        cuentas = Cuenta.objects.filter(estado=1).order_by('id')
        page = self.paginate_queryset(cuentas, request)

        if page is not None:
            serializer = CuentaSerializer(page, many=True)
            logger.info("Paginated response for cuentas")
            return self.get_paginated_response(serializer.data)

        serializer = CuentaSerializer(cuentas, many=True)
        logger.error("Returning all cuentas without pagination")
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(request_body=CuentaSerializer, responses={201: CuentaSerializer()})
    def post(self, request):
        """
        Crear una nueva cuenta.
        """
        logger.info("POST request to create a new cuenta")
        serializer = CuentaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            logger.info("New cuenta created successfully")
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        logger.error("Failed to create cuenta: %s", serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CuentaDetails(APIView):
    """
    Vista para obtener, actualizar o eliminar una cuenta especifica.
    """
    permission_classes = [IsAuthenticated, CustomPermission]
    model = Cuenta
    @swagger_auto_schema(responses={200: CuentaSerializer()})
    def get(self, request, pk):
        """
        Obtener una cuenta especifica por su ID.
        """
        logger.info("GET request to obtain cuenta with ID: %s", pk)
        cuenta=get_object_or_404(Cuenta, id=pk, estado=1)
        if not cuenta:
            return Response({'Error': 'Cuenta no encontrada'}, status=status.HTTP_404_NOT_FOUND)
        serializer = CuentaSerializer(cuenta)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(request_body=CuentaSerializer, responses={200: CuentaSerializer()})
    def put(self, request, pk):
        """
        Actualizar completamente una cuenta por su ID.
        """
        logger.info("PUT request to update cuenta with ID: %s", pk)
        cuenta = get_object_or_404(Cuenta, id=pk, estado=1)
        if not cuenta:
            return Response({'Error': 'Cuenta no encontrada'}, status=status.HTTP_404_NOT_FOUND)
        self.check_object_permissions(request, cuenta) # Verificación de permisos
        serializer = CuentaSerializer(cuenta, data=request.data)
        if serializer.is_valid():
            serializer.save()
            logger.info("Cuenta updated successfully with ID: %s", pk)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        logger.error("Failed to update cuenta with ID: %s. Errors: %s", pk, serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(request_body=CuentaSerializer, responses={200: CuentaSerializer()})
    def patch(self, request, pk):
        """
        Actualizar parcialmente una cuenta por su ID.
        """
        logger.info("PATCH request to partially update cuenta with ID: %s", pk)
        cuenta = get_object_or_404(Cuenta, id=pk, estado=1)
        if not cuenta:
            return Response({'Error': 'Cuenta no encontrada'}, status=status.HTTP_404_NOT_FOUND)
        self.check_object_permissions(request, cuenta) # Verificación de permisos
        serializer = CuentaSerializer(cuenta, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            logger.info("Cuenta partially updated successfully with ID: %s", pk)
            return Response(serializer.data, status=status.HTTP_200_OK)
        logger.error("Failed to partially update cuenta with ID: %s. Errors: %s", pk, serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(responses={204: 'No Content'})
    def delete(self, request, pk):
        """
        Eliminar una cuenta por su ID.
        """
        logger.info("DELETE request to delete cuenta with ID: %s", pk)
        cuenta=get_object_or_404(Cuenta, id=pk, estado=1)
        if not cuenta:
            return Response({'Error': 'Cuenta no encontrada'}, status=status.HTTP_404_NOT_FOUND)
        self.check_object_permissions(request, cuenta)
        cuenta.estado = 0
        cuenta.save()
        logger.info("Departamento deleted successfully with ID: %s", pk)
        return Response(status=status.HTTP_204_NO_CONTENT)