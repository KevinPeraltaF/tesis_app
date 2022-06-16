import sys

from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from django.template.loader import get_template

from tesis.forms import ClaseForm
from tesis.models import Clase


def Dashboard(request):
    global ex
    data = {}
    if request.method == 'POST':
        if 'peticion' in request.POST:
            peticion = request.POST['peticion']
            if peticion == 'crear_clase':
                try:
                    form = ClaseForm(request.POST, request.FILES)
                    if form.is_valid():
                        nombre = form.cleaned_data['nombre']
                        seccion = form.cleaned_data['seccion']
                        materia = form.cleaned_data['materia']
                        aula = form.cleaned_data['aula']

                        clase = Clase(
                            nombre=nombre,
                            seccion=seccion,
                            materia=materia,
                            aula=aula,
                            archivada=False

                        )
                        clase.save(request)

                        return JsonResponse({"result": True}, safe=False)
                    else:
                        return JsonResponse( {"respuesta": False, "mensaje": "Ha ocurrido un error al enviar los datos."})


                except Exception as ex:
                    transaction.set_rollback(True)
                    return JsonResponse({"respuesta": False, "mensaje": "Ha ocurrido un error, intente mas tarde."})

            if peticion == 'crear_clase':
                try:
                    form = ClaseForm(request.POST, request.FILES)
                    if form.is_valid():
                        nombre = form.cleaned_data['nombre']
                        seccion = form.cleaned_data['seccion']
                        materia = form.cleaned_data['materia']
                        aula = form.cleaned_data['aula']
                        clase = Clase(
                            nombre=nombre,
                            seccion=seccion,
                            materia=materia,
                            aula=aula,
                            archivada=False

                        )
                        clase.save(request)
                        return JsonResponse({"result": False}, safe=False)

                except Exception as ex:
                    transaction.set_rollback(True)
                    return JsonResponse({"result": True, "mensaje": "Datos erróneos, intente nuevamente."}, safe=False)
    else:
        if 'peticion' in request.GET:
            peticion = request.GET['peticion']

            if peticion == 'crear_clase':
                try:
                    form = ClaseForm()
                    data['form'] = form
                    data['peticion'] = 'crear_clase'
                    template = get_template("clase/crear_clase.html")
                    return JsonResponse({"respuesta": True, 'data': template.render(data)})
                except Exception as ex:
                    pass


        else:
            try:
                data['titulo'] = 'Menú principal'

                return render(request, "registration/dashboard.html ", data)
            except Exception as ex:
                print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno))

def Login(request):
    global ex
    data = {}
    if request.method == 'POST':
        if 'peticion' in request.POST:
            peticion = request.POST['peticion']
    else:
        if 'peticion' in request.GET:
            peticion = request.GET['peticion']

        else:
            try:
                data['titulo'] = 'Inicio de Sesion'

                return render(request, "registration/login.html ", data)
            except Exception as ex:
                print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno))

