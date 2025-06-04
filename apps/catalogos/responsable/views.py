from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Responsable
from .serializers import ResponsableSerializer
from drf_yasg.utils import swagger_auto_schema
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from ...permissions import CustomPermission
from config.utils.Pagination import PaginationMixin
import logging.handlers

# Configura el logger
logger = logging.getLogger(__name__)

# Create your views here.
class ResponsableApiView(PaginationMixin, APIView):
    """
    Vista para listar todos los responsables o crear un nuevo responsable
    """
    #permission_classes = [IsAuthenticated, CustomPermission]
    model=Responsable

    @swagger_auto_schema(responses={200: ResponsableSerializer(many=True)})
    def get(self, request):
        """
        Listar todos los responsables.
        """
        logger.info("GET request to list all departamentos")
        responsable = Responsable.objects.filter(estado=1).order_by('id')
        page = self.paginate_queryset(responsable, request)

        if page is not None:
            serializer = ResponsableSerializer(page, many=True)
            logger.info("Paginated response for responsables")
            return self.get_paginated_response(serializer.data)

        serializer = ResponsableSerializer(responsable, many=True)
        logger.info("Returning all departamentos without pagination")
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(request_body=ResponsableSerializer, responses={201: ResponsableSerializer()})
    def post(self, request):
        """
        Crear un nuevo responsable.
        """
        logger.info("POST request to create a new responsable")
        serializer = ResponsableSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            logger.info("Responsable created successfully")
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        logger.error("Failed to create responsable: %s", serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ResponsableDetails(APIView):
    """
    Vista para obtener, actualizar o eliminar un responsable especifico.
    """
    #permission_classes = [IsAuthenticated, CustomPermission]
    model=Responsable

    @swagger_auto_schema(responses={200: ResponsableSerializer()})
    def get(self, request, pk):
        """
        Obtener un responsable especifico por su ID.
        """
        logger.info("GET request to obtain anio with ID: %s", pk)
        responsable = get_object_or_404(Responsable, id=pk, estado=1)
        if not responsable:
            return Response({'Error':'Responsable no encontrado.'},status=status.HTTP_404_NOT_FOUND)
        serializer = ResponsableSerializer(responsable)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(request_body=ResponsableSerializer, responses={200: ResponsableSerializer()})
    def put(self, request, pk):
        """
        Actualizar completamente un responsable por su ID.
        """
        logger.info("PUT request to update responsable with ID: %s", pk)

        responsable = get_object_or_404(Responsable, id=pk, estado=1)
        if not responsable:
            return Response({'Error':'Responsable no encontrado.'},status=status.HTTP_404_NOT_FOUND)
        self.check_object_permissions(request, responsable)
        serializer = ResponsableSerializer(responsable, data=request.data)
        if serializer.is_valid():
            serializer.save()
            logger.info("Responsable updated successfully with ID: %s", pk)
            return Response(serializer.data)
        logger.error("Failed to update responsable with ID: %s. Errors: %s", pk, serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(request_body=ResponsableSerializer, responses={200: ResponsableSerializer()})
    def patch(self, request, pk):
        """
        Actualizar parcialmente un responsable por su ID.
        """
        logger.info("PATCH request to partially update responsable with ID: %s", pk)
        responsable = get_object_or_404(Responsable, id=pk, estado=1)
        if not responsable:
            return Response({'Error':'Responsable no encontrado.'},status=status.HTTP_404_NOT_FOUND)
        self.check_object_permissions(request, responsable)
        serializer = ResponsableSerializer(responsable, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            logger.info("Responsable partially updated successfully with ID: %s", pk)
            return Response(serializer.data)
        logger.error("Failed to partially update responsable with ID: %s. Errors: %s", pk, serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(responses={204: 'No Content'})
    def delete(self, request, pk):
        """
        Eliminar un responsable por su ID.
        """
        logger.info("DELETE request to delete responsable with ID: %s", pk)
        responsable = get_object_or_404(Responsable, id=pk, estado=1)
        if not responsable:
            return Response({'Error':'Responsable no encontrado.'},status=status.HTTP_404_NOT_FOUND)
        self.check_object_permissions(request, responsable)
        responsable.estado=0
        responsable.save()
        logger.info("Responsable deleted successfully with ID: %s", pk)
        return Response(status=status.HTTP_204_NO_CONTENT)


