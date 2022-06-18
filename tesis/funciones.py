def Data_inicial(request,data):
    from tesis.models import Clase
    data['clases'] = clases = Clase.objects.filter(status=True, archivada=False,usuario_creacion = request.user)
