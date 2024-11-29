from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from tutorial.quickstart.serializers import UserSerializer

from .models import User
from .serializers import UserCreateSerializer
from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import IsAuthenticated # Para proteger la vista
from ...permissions import CustomPermission

# Create your views here.
class UserCreateView(APIView):
    permission_classes = [IsAuthenticated, CustomPermission]
    model = User

    @swagger_auto_schema(responses={200: UserCreateSerializer(many=True)})
    def get(self,request):
        usuario=User.objects.all()
        serializer = UserCreateSerializer(usuario, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


    @swagger_auto_schema(request_body=UserCreateSerializer, responses={201: UserCreateSerializer()})
    def post(self,request):
        serializer = UserCreateSerializer(data=request.data)

        # Validar los datos
        if serializer.is_valid():
            serializer.save() # Crear el usuario
            return Response({'Mensaje':'Usuario creado exitosamente.'}, status=status.HTTP_201_CREATED)

        # En caso de error, retornar las validaciones
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
