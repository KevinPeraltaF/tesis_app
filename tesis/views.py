import sys
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db import transaction
from django.forms import model_to_dict
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render, redirect

# Create your views here.
from django.template.loader import get_template

from tesis.forms import ClaseForm, RegistroUsuarioForm, UnirmeClaseForm
from tesis.funciones import Data_inicial
from tesis.models import Clase, Persona, ClaseInscrita


@login_required(redirect_field_name='next', login_url='/login')
@transaction.atomic()
def Dashboard(request):
    global ex
    data = {}
    Data_inicial(request, data)
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
                        generador_codigo_clase = User.objects.make_random_password(length=7)
                        while Clase.objects.filter(codigo_clase=generador_codigo_clase).exists():
                            generador_codigo_clase = User.objects.make_random_password(length=7)

                        clase = Clase(
                            nombre=nombre,
                            seccion=seccion,
                            materia=materia,
                            aula=aula,
                            archivada=False,
                            codigo_clase=generador_codigo_clase
                        )
                        clase.save(request)

                        return redirect('/')
                    else:
                        return render(request, "registration/dashboard.html", {'form': form})


                except Exception as ex:
                    transaction.set_rollback(True)
                    return JsonResponse({"respuesta": False, "mensaje": "Ha ocurrido un error, intente mas tarde."})

            if peticion == 'unirme_a_clase':
                try:
                    form = UnirmeClaseForm(request.POST, request.FILES)
                    if form.is_valid():

                        codigo_clase = form.cleaned_data['codigo_clase']
                        usuario = request.user
                        if Clase.objects.filter(codigo_clase=codigo_clase).exists():
                            clase = Clase.objects.get(codigo_clase=codigo_clase)
                            if not clase.usuario_creacion == usuario:
                                clase_inscrita = ClaseInscrita(
                                    usuario=usuario,
                                    clase=clase,

                                )
                                clase_inscrita.save(request)

                            return redirect('/clase/?peticion=estudiante_ver_clase&id=%s' % clase.pk)
                        else:
                            return JsonResponse(
                                {"respuesta": False, "mensaje": "El código que ingreso es incorrecto."})


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
                        return redirect('/')
                    else:
                        return render(request, "registration/dashboard.html", {'form': form, })


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
                    data['obtener_clase'] = clase = Clase.objects.get(pk=request.GET['id'])
                    form = ClaseForm(initial=model_to_dict(clase))
                    data['form'] = form
                    data['peticion'] = 'editar_clase'
                    template = get_template("clase/formClase.html")
                    return JsonResponse({"respuesta": True, 'data': template.render(data)})
                except Exception as ex:
                    pass

            if peticion == 'unirme_a_clase':
                try:
                    form = UnirmeClaseForm()
                    data['form'] = form
                    data['peticion'] = 'unirme_a_clase'
                    template = get_template("clase/formUnirmeClase.html")
                    return JsonResponse({"respuesta": True, 'data': template.render(data)})
                except Exception as ex:
                    pass


        else:
            try:
                data['titulo'] = 'Menú principal'

                return render(request, "registration/dashboard.html", data)
            except Exception as ex:
                print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno))
                pass


@transaction.atomic()
def Login(request):
    global ex
    data = {}
    if request.method == 'POST':
        if 'peticion' in request.POST:
            peticion = request.POST['peticion']
            if peticion == 'login_usuario':
                try:
                    usuario = authenticate(username=request.POST['usuario'].lower().strip(),
                                           password=request.POST['clave'])
                    if usuario is not None:
                        if usuario.is_active:
                            login(request, usuario)
                            return JsonResponse({"respuesta": True})
                        else:
                            return JsonResponse(
                                {"respuesta": False, 'mensaje': u'Inicio de sesión incorrecto, usuario no activo.'})
                    else:
                        return JsonResponse({"respuesta": False,
                                             'mensaje': u'Inicio de sesión incorrecto, usuario o clave no coinciden.'})
                except Exception as ex:
                    transaction.set_rollback(True)
                    return JsonResponse(
                        {"respuesta": False, "mensaje": "Error al iniciar sesión, intentelo más tarde."})
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
                pass


def Logout(request):
    logout(request)
    return HttpResponseRedirect("/login")


@transaction.atomic()
def registrate(request):
    global ex
    data = {}
    if request.method == 'POST':
        if 'peticion' in request.POST:
            peticion = request.POST['peticion']
            if peticion == 'registrate':
                try:
                    if request.session.get('id') != None:  # Regístrese solo cuando no haya iniciado sesión
                        return JsonResponse({"respuesta": False, "mensaje": "Ya tiene sesión iniciada."})
                    form = RegistroUsuarioForm(request.POST)

                    if form.is_valid():
                        username = form.cleaned_data['username']
                        password = form.cleaned_data['password1']
                        nombre1 = form.cleaned_data['nombre1']
                        nombre2 = form.cleaned_data['nombre2']
                        apellido1 = form.cleaned_data['apellido1']
                        apellido2 = form.cleaned_data['apellido2']
                        email = form.cleaned_data['email']
                        username = username.strip()  # Eliminar espacios y líneas nuevas
                        password = password.strip()
                        usuario = User.objects.create_user(username, '', password)
                        usuario.save()

                        persona = Persona(
                            usuario=usuario,
                            nombre1=nombre1,
                            nombre2=nombre2,
                            apellido1=apellido1,
                            apellido2=apellido2,
                            email=email,
                        )
                        persona.save(request)
                        return redirect('/login/')

                    else:
                        return render(request, "registration/registrate.html", {'form': form})
                except Exception as ex:
                    transaction.set_rollback(True)
                    return JsonResponse({"respuesta": False, "mensaje": "Ha ocurrido un error, intente mas tarde."})
        return JsonResponse({"respuesta": False, "mensaje": "No se ha encontrado respuesta."})

    else:
        data['form'] = RegistroUsuarioForm()

    return render(request, "registration/registrate.html", data)
