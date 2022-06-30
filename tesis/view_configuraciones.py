import sys
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import render
from django.template.loader import get_template

from tesis.funciones import Data_inicial
from tesis.models import MetodoCalificacion, DetalleMetodoCalificacion, CampoDetalleMetodoCalificacion


@login_required(redirect_field_name='next', login_url='/login')
@transaction.atomic()
def Configuraciones(request):
    global ex
    data = {}
    Data_inicial(request, data)
    if request.method == 'POST':
        if 'peticion' in request.POST:
            peticion = request.POST['peticion']

    else:
        if 'peticion' in request.GET:
            peticion = request.GET['peticion']

            if peticion == 'metodo_calificacion':
                try:
                    data['metodoCalificacion'] = metodoCalificacion = MetodoCalificacion.objects.filter(status=True)

                    return render(request, "configuraciones/metodocalificacion.html", data)
                except Exception as ex:
                    pass

            if peticion == 'ver_modelo_calificacion':
                try:
                    modelo = MetodoCalificacion.objects.get(pk=request.GET['id'])
                    data['modelo'] = modelo
                    template = get_template("configuraciones/modal/ver_detalle_metodo_calificacion.html")
                    return JsonResponse({"respuesta": True, 'data': template.render(data)})
                except Exception as ex:
                    pass

            if peticion == 'agregar_detalle_modelo':
                try:
                    detalle = DetalleMetodoCalificacion.objects.filter(modelo_id=request.GET['id'],status=True)
                    data['modelo'] = detalle
                    return render(request, "configuraciones/detalle.html", data)
                except Exception as ex:
                    pass

            if peticion == 'agregar_campo_detalle_modelo':
                try:
                    campo = CampoDetalleMetodoCalificacion.objects.filter(detallemetodocalificacion_id=request.GET['id'],status=True)
                    data['campo'] = campo
                    return render(request, "configuraciones/campo.html", data)
                except Exception as ex:
                    pass

        else:
            try:
                data['titulo'] = 'Menú principal'
                return render(request, "configuraciones/view.html", data)
            except Exception as ex:
                print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno))
                pass
