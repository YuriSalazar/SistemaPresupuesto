from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Mes
from .serializers import MesSerializer
from drf_yasg.utils import swagger_auto_schema
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from ...permissions import CustomPermission
from config.utils.Pagination import PaginationMixin
import logging.handlers

# Configura el logger
logger = logging.getLogger(__name__)

# Create your views here.
class MesApiView(PaginationMixin, APIView):
    """
    Vista para listar todos los meses o crear un nuevo mes
    """
    permission_classes = [IsAuthenticated,CustomPermission]
    model = Mes

    @swagger_auto_schema(responses={200: MesSerializer(many=True)})
    def get(self, request):
        """
        Listar todos los meses.
        """
        logger.info("GET request to list all meses")
        mes = Mes.objects.all().order_by('id')
        page=self.paginate_queryset(mes, request)

        if page is not None:
            serializer = MesSerializer(page, many=True)
            logger.info("Paginated response for mes")
            return self.get_paginated_response(serializer.data)

        serializer = MesSerializer(mes, many=True)
        logger.error("Returning all meses without pagination")
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(request_body=MesSerializer, responses={201: MesSerializer()})
    def post(self, request):
        """
        Crear un nuevo mes.
        """
        logger.info("POST request to create new mes")

        serializer = MesSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            logger.info("New mes created successfully")
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        logger.error("Failed to create mes: %s", serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class MesDetails(APIView):
    """
    Vista para obtener, actualizar o eliminar un mes especifico.
    """
    permission_classes = [IsAuthenticated,CustomPermission]
    model = Mes

    @swagger_auto_schema(responses={200: MesSerializer()})
    def get(self, request, pk):
        """
        Obtener un mes especifico por su ID.
        """
        logger.info("GET request to obtain mes with ID: %s", pk)
        mes=get_object_or_404(Mes, id=pk)

        if not mes:
            return Response({'Error':'Mes no encontrado.'},status=status.HTTP_404_NOT_FOUND)
        serializer = MesSerializer(mes)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(request_body=MesSerializer, responses={200: MesSerializer()})
    def put(self, request, pk):
        """
        Actualizar completamente un mes por su ID.
        """
        logger.info("PUT request to update mes with ID: %s", pk)
        mes=get_object_or_404(Mes, id=pk)

        if not mes:
            return Response({'Error':'Mes no encontrado.'},status=status.HTTP_404_NOT_FOUND)
        self.check_object_permissions(request, mes)
        serializer = MesSerializer(mes, data=request.data)
        if serializer.is_valid():
            serializer.save()
            logger.info("Mes updated successfully with ID: %s", pk)
            return Response(serializer.data)
        logger.error("Failed to update mes: %s", serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(request_body=MesSerializer, responses={200: MesSerializer()})
    def patch(self, request, pk):
        """
        Actualizar parcialmente un mes por su ID.
        """
        logger.info("PATCH request to partially update mes with ID: %s", pk)
        mes=get_object_or_404(Mes, id=pk)
        if not mes:
            return Response({'Error':'Mes no encontrado.'},status=status.HTTP_404_NOT_FOUND)
        self.check_object_permissions(request, mes)
        serializer = MesSerializer(mes, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            logger.info("Mes partially updated successfully with ID: %s", pk)
            return Response(serializer.data)
        logger.error("Failed to partially update mes with ID: %s. Errors: %s", pk, serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(responses={204: 'No Content'})
    def delete(self, request, pk):
        """
        Eliminar un mes por su ID.
        """
        logger.info("DELETE request to delete mes with ID: %s", pk)
        mes = get_object_or_404(Mes, id=pk)
        if not mes:
            return Response({'Error':'Mes no encontrado.'},status=status.HTTP_404_NOT_FOUND)
        self.check_object_permissions(request, mes)
        mes.delete()
        logger.info("Mes deleted successfully with ID: %s", pk)
        return Response(status=status.HTTP_204_NO_CONTENT)
