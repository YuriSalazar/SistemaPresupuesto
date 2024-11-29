from rest_framework.permissions import BasePermission

class CustomPermission(BasePermission):
    """
    Permiso personalizado para cualquier modelo.
    Verificar si el usuario tiene los permisos estandar (view, add, change, delete) dinamicamente
    segun el modelo y la aplicacion.
    """
    def has_permission(self, request, view):
        """
        Verifica permisos para operaciones de lista y creacion (GET, POST).
        Intente obtener el modelo desde "get_queryset()" o directametne desde la vista.
        """
        # Intentar obtener el modelo dinamicamente
        if hasattr(view, 'queryset') and view.queryset is not None:
            model=view.queryset.model
        elif hasattr(view, 'get_queryset'):
            model=view.get_queryset().model
        else:
            # Especificar explicitamente el modelo desde la vista si no eta disponible en el queryset
            model=getattr(view, 'model', None)
            if model is None:
                raise AttributeError('No se puede obtener el modelo para verificar los permisos.')

        # Para operaciones de lista (GET) y creacion (POST)
        if request.method=='GET':
            return request.user.has_perm(f'{model._meta.app_label}.view_{model._meta.model_name}')
        if request.method=='POST':
            return request.user.has_perm(f'{model._meta.app_label}.add_{model._meta.model_name}')
        return True

    def has_object_permission(self, request, view, obj):
        """
        Verifica permisos para operaciones sobre un objeto especifico (PUT, PATCH, DELETE).
        """
        # Para las operaciones que modifican o eliminan objetos (PUT, PATCH, DELETE)
        if request.method in ['PUT', 'PATCH']:
            return request.user.has_perm(f'{obj._meta.app_label}.change_{obj._meta.model_name}')
        if request.method=='DELETE':
            return request.user.has_perm(f'{obj._meta.app_label}.delete_{obj._meta.model_name}')
        return True
