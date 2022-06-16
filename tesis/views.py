import sys

from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.forms import model_to_dict
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from django.template.loader import get_template

from tesis.forms import ClaseForm
from tesis.models import Clase

@login_required(redirect_field_name='next', login_url='/login')
@transaction.atomic()
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

                        return render(request, "registration/dashboard.html ", data)
                    else:
                        return render(request, "registration/dashboard.html", {'form': form})


                except Exception as ex:
                    transaction.set_rollback(True)
                    return JsonResponse({"respuesta": False, "mensaje": "Ha ocurrido un error, intente mas tarde."})

            if peticion == 'editar_clase':
                try:
                    form = ClaseForm(request.POST, request.FILES)
                    if form.is_valid():
                        nombre = form.cleaned_data['nombre']
                        seccion = form.cleaned_data['seccion']
                        materia = form.cleaned_data['materia']
                        aula = form.cleaned_data['aula']

                        clase = Clase.objects.get(pk=request.POST['id'])
                        clase.nombre = nombre
                        clase.seccion = seccion
                        clase.materia = materia
                        clase.aula = aula
                        clase.save(request)
                        return render(request, "registration/dashboard.html ", data)
                    else:
                        return render(request, "registration/dashboard.html", {'form': form,})


                except Exception as ex:
                    transaction.set_rollback(True)
                    return JsonResponse({"respuesta": False, "mensaje": "Ha ocurrido un error, intente mas tarde."})


        if peticion == 'archivar_clase':
            try:
                with transaction.atomic():
                    registro = Clase.objects.get(pk=request.POST['id'])
                    registro.archivada = True
                    registro.save(request)
                    return JsonResponse({"respuesta": True, "mensaje": "Clase archivada correctamente."})

            except Exception as ex:
                pass

        if peticion == 'restaurar_clase':
            try:
                with transaction.atomic():
                    registro = Clase.objects.get(pk=request.POST['id'])
                    registro.archivada = False
                    registro.save(request)
                    return JsonResponse({"respuesta": True, "mensaje": "Clase archivada correctamente."})

            except Exception as ex:
                pass

    else:
        if 'peticion' in request.GET:
            peticion = request.GET['peticion']

            if peticion == 'crear_clase':
                try:
                    form = ClaseForm()
                    data['form'] = form
                    data['peticion'] = 'crear_clase'
                    template = get_template("clase/formClase.html")
                    return JsonResponse({"respuesta": True, 'data': template.render(data)})
                except Exception as ex:
                    pass

            if peticion == 'editar_clase':
                try:
                    data['clase'] = clase = Clase.objects.get(pk=request.GET['id'])
                    form = ClaseForm(initial=model_to_dict(clase))
                    data['form'] = form
                    data['peticion'] = 'editar_clase'
                    template = get_template("clase/formClase.html")
                    return JsonResponse({"respuesta": True, 'data': template.render(data)})
                except Exception as ex:
                    pass

            if peticion == 'clases_archivadas':
                try:
                    data['peticion'] = 'clases_archivadas'
                    data['clases'] = clases = Clase.objects.filter(status=True, archivada=False)
                    data['clases_archivadas'] = clases_archivadas = Clase.objects.filter(status=True, archivada=True)
                    return render(request, "clase/clases_Archivadas.html ", data)
                except Exception as ex:
                    print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno))


        else:
            try:
                data['titulo'] = 'Menú principal'

                data['clases'] = clases = Clase.objects.filter(status=True, archivada=False)

                return render(request, "registration/dashboard.html ", data)
            except Exception as ex:
                print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno))

@transaction.atomic()
def Login(request):
    global ex
    data = {}
    if request.method == 'POST':
        if 'peticion' in request.POST:
            peticion = request.POST['peticion']
            if peticion == 'login_usuario':
                try:
                    usuario = authenticate(username=request.POST['usuario'].lower().strip(), password=request.POST['clave'])
                    if usuario is not None:
                        if usuario.is_active:
                            login(request, usuario)
                            return JsonResponse({"respuesta": True})
                        else:
                            return JsonResponse({"respuesta": False, 'mensaje': u'Inicio de sesión incorrecto, usuario no activo.'})
                    else:
                        return JsonResponse({"respuesta": False,'mensaje': u'Inicio de sesión incorrecto, usuario o clave no coinciden.'})
                except Exception as ex:
                    transaction.set_rollback(True)
                    return JsonResponse({"respuesta": False, "mensaje": "Error al iniciar sesión, intentelo más tarde."})
        return JsonResponse({"respuesta": False, "mensaje": "acción Incorrecta."})
    else:
        if 'peticion' in request.GET:
            peticion = request.GET['peticion']
        else:
            try:
                if 'persona' in request.session:
                    return HttpResponseRedirect("/")
                data['titulo'] = 'Inicio de sesión'
                data['request'] = request
                return render(request, "registration/login.html", data)
            except Exception as ex:
                print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno))


def Logout(request):
    logout(request)
    return HttpResponseRedirect("/login")
