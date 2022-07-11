import sys
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.template.loader import get_template

from tesis.forms import MetodoCalifcacionForm, DetalleMetodoCalificacionForm, CampoDetalleMetodoCalificacionForm, \
    ClaseForm, UnirmeClaseForm, PersonaForm
from tesis.funciones import Data_inicial
from tesis.models import MetodoCalificacion, DetalleMetodoCalificacion, CampoDetalleMetodoCalificacion, Persona, Clase, \
    ClaseInscrita


@login_required(redirect_field_name='next', login_url='/login')
@transaction.atomic()
def Configuraciones(request):
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
                        metodocalificacion = form.cleaned_data['metodocalificacion']

                        generador_codigo_clase = User.objects.make_random_password(length=7)
                        while Clase.objects.filter(codigo_clase=generador_codigo_clase).exists():
                            generador_codigo_clase = User.objects.make_random_password(length=7)

                        clase = Clase(
                            nombre=nombre,
                            seccion=seccion,
                            materia=materia,
                            aula=aula,
                            archivada=False,
                            codigo_clase=generador_codigo_clase,
                            modelo=metodocalificacion
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

            if peticion == 'addmetodocalificacion':
                try:
                    form = MetodoCalifcacionForm(request.POST, request.FILES)
                    if form.is_valid():
                        nombre = form.cleaned_data['nombre']
                        nota_aprobacion = form.cleaned_data['nota_aprobacion']

                        registro = MetodoCalificacion(
                            nombre=nombre,
                            nota_aprobacion=nota_aprobacion

                        )
                        registro.save(request)



                        return redirect("/configuracion/?peticion=metodo_calificacion")
                    else:
                        return redirect("/configuracion/?peticion=metodo_calificacion")


                except Exception as ex:
                    transaction.set_rollback(True)
                    return JsonResponse({"respuesta": False, "mensaje": "Ha ocurrido un error, intente mas tarde."})

            if peticion == 'addmetodocalificaciondetalle':
                id= 0
                try:
                    id = request.POST['id']
                    form = DetalleMetodoCalificacionForm(request.POST, request.FILES)
                    if form.is_valid():
                        modelo =id
                        nombre = form.cleaned_data['nombre']
                        nota_aprobacion = form.cleaned_data['nota_aprobacion']

                        registro = DetalleMetodoCalificacion(
                            modelo_id =modelo,
                            nombre=nombre,
                            nota_aprobacion=nota_aprobacion

                        )
                        registro.save(request)



                        return redirect("/configuracion/?peticion=agregar_detalle_modelo&id=%s"% id)
                    else:
                        return redirect("/configuracion/?peticion=agregar_detalle_modelo&id=%s"% id)


                except Exception as ex:
                    transaction.set_rollback(True)
                    return JsonResponse({"respuesta": False, "mensaje": "Ha ocurrido un error, intente mas tarde."})

            if peticion == 'addmetodocalificacioncampo':
                id= 0
                try:
                    id = request.POST['id']
                    form = CampoDetalleMetodoCalificacionForm(request.POST, request.FILES)
                    if form.is_valid():
                        modelo =id
                        nombre = form.cleaned_data['nombre']
                        nota_aprobacion = form.cleaned_data['nota_aprobacion']

                        registro = CampoDetalleMetodoCalificacion(
                            detallemetodocalificacion_id =modelo,
                            nombre=nombre,
                            nota_aprobacion=nota_aprobacion

                        )
                        registro.save(request)



                        return redirect("/configuracion/?peticion=agregar_campo_detalle_modelo&id=%s"% id)
                    else:
                        return redirect("/configuracion/?peticion=agregar_campo_detalle_modelo&id=%s"% id)


                except Exception as ex:
                    transaction.set_rollback(True)
                    return JsonResponse({"respuesta": False, "mensaje": "Ha ocurrido un error, intente mas tarde."})

            if peticion == 'eliminar_metodo_calificacion':
                try:
                    with transaction.atomic():
                        registro = MetodoCalificacion.objects.get(pk=request.POST['id'])
                        registro.status = False
                        registro.save(request)
                        return JsonResponse({"respuesta": True, "mensaje": "Registro eliminado correctamente."})

                except Exception as ex:
                    pass

            if peticion == 'eliminar_detalle_calificacion':
                try:
                    with transaction.atomic():
                        registro = DetalleMetodoCalificacion.objects.get(pk=request.POST['id'])
                        registro.status = False
                        registro.save(request)
                        return JsonResponse({"respuesta": True, "mensaje": "Registro eliminado correctamente."})

                except Exception as ex:
                    pass

            if peticion == 'eliminar_campo_calificacion':
                try:
                    with transaction.atomic():
                        registro = CampoDetalleMetodoCalificacion.objects.get(pk=request.POST['id'])
                        registro.status = False
                        registro.save(request)
                        return JsonResponse({"respuesta": True, "mensaje": "Registro eliminado correctamente."})

                except Exception as ex:
                    pass

            if peticion == 'editar_metodo_calificacion':
                try:
                    form = MetodoCalifcacionForm(request.POST, request.FILES)
                    metodo = MetodoCalificacion.objects.get(pk=request.POST['id'])

                    if form.is_valid():
                        nombre = form.cleaned_data['nombre']
                        nota_aprobacion = form.cleaned_data['nota_aprobacion']

                        metodo.nombre = nombre
                        metodo.nota_aprobacion = nota_aprobacion
                        metodo.save(request)


                        return redirect("/configuracion/?peticion=metodo_calificacion" )
                    else:
                        return redirect("/configuracion/?peticion=metodo_calificacion")


                except Exception as ex:
                    transaction.set_rollback(True)
                    return JsonResponse({"respuesta": False, "mensaje": "Ha ocurrido un error, intente mas tarde."})

            if peticion == 'editar_detalle_calificacion':
                try:
                    form = DetalleMetodoCalificacionForm(request.POST, request.FILES)
                    metodo = DetalleMetodoCalificacion.objects.get(pk=request.POST['id'])

                    if form.is_valid():
                        nombre = form.cleaned_data['nombre']
                        nota_aprobacion = form.cleaned_data['nota_aprobacion']

                        metodo.nombre = nombre
                        metodo.nota_aprobacion = nota_aprobacion
                        metodo.save(request)

                        return redirect("/configuracion/?peticion=agregar_detalle_modelo&id=%s"% metodo.modelo.pk )
                    else:
                        return redirect("/configuracion/?peticion=agregar_detalle_modelo&id=%s"% metodo.modelo.pk)


                except Exception as ex:
                    transaction.set_rollback(True)
                    return JsonResponse({"respuesta": False, "mensaje": "Ha ocurrido un error, intente mas tarde."})

            if peticion == 'editar_campo_calificacion':
                try:
                    form = CampoDetalleMetodoCalificacionForm(request.POST, request.FILES)
                    metodo = CampoDetalleMetodoCalificacion.objects.get(pk=request.POST['id'])

                    if form.is_valid():
                        nombre = form.cleaned_data['nombre']
                        nota_aprobacion = form.cleaned_data['nota_aprobacion']

                        metodo.nombre = nombre
                        metodo.nota_aprobacion = nota_aprobacion
                        metodo.save(request)

                        return redirect("/configuracion/?peticion=agregar_campo_detalle_modelo&id=%s"% metodo.detallemetodocalificacion.pk)
                    else:
                        return redirect("/configuracion/?peticion=agregar_campo_detalle_modelo&id=%s"% metodo.detallemetodocalificacion.pk)


                except Exception as ex:
                    transaction.set_rollback(True)
                    return JsonResponse({"respuesta": False, "mensaje": "Ha ocurrido un error, intente mas tarde."})

    else:
        if 'peticion' in request.GET:
            peticion = request.GET['peticion']

            if peticion == 'profesor':
                try:
                    data['profesor'] = Persona.objects.filter(status=True, usuario__groups__id= 1)#1 profesor
                    return render(request, "profesor/view.html", data)
                except Exception as ex:
                    pass

            if peticion == 'crear_profesor':
                try:
                    form =PersonaForm()
                    data['form'] = form
                    data['peticion'] = 'crear_profesor'
                    template = get_template("profesor/modal/crear_profesor.html")
                    return JsonResponse({"respuesta": True, 'data': template.render(data)})
                except Exception as ex:
                    pass


            if peticion == 'metodo_calificacion':
                try:
                    metodoCalificacion = MetodoCalificacion.objects.filter(status=True)
                    paginator = Paginator(metodoCalificacion, 15)
                    page_number = request.GET.get('page')
                    page_obj = paginator.get_page(page_number)
                    data['metodoCalificacion'] = page_obj

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
                    detalle = DetalleMetodoCalificacion.objects.filter(modelo_id=request.GET['id'], status=True)
                    data['padre'] = request.GET['id']

                    paginator = Paginator(detalle, 15)
                    paginator = Paginator(detalle, 15)
                    page_number = request.GET.get('page')
                    page_obj = paginator.get_page(page_number)
                    data['modelo'] = page_obj

                    return render(request, "configuraciones/detalle.html", data)
                except Exception as ex:
                    pass

            if peticion == 'agregar_campo_detalle_modelo':
                try:
                    campo = CampoDetalleMetodoCalificacion.objects.filter(
                        detallemetodocalificacion_id=request.GET['id'], status=True)
                    data['padre'] = request.GET['id']

                    paginator = Paginator(campo, 15)
                    page_number = request.GET.get('page')
                    page_obj = paginator.get_page(page_number)
                    data['campo'] = page_obj

                    return render(request, "configuraciones/campo.html", data)
                except Exception as ex:
                    pass

            if peticion == 'addmetodocalificacion':
                try:
                    form = MetodoCalifcacionForm()
                    data['form'] = form
                    data['peticion'] = 'addmetodocalificacion'
                    template = get_template("configuraciones/modal/metodocalificacion.html")
                    return JsonResponse({"respuesta": True, 'data': template.render(data)})
                except Exception as ex:
                    pass

            if peticion == 'addmetodocalificaciondetalle':
                try:
                    form = DetalleMetodoCalificacionForm()
                    data['form'] = form
                    data['padre'] = request.GET['id']
                    data['peticion'] = 'addmetodocalificaciondetalle'
                    template = get_template("configuraciones/modal/metodocalificaciondetalle.html")
                    return JsonResponse({"respuesta": True, 'data': template.render(data)})
                except Exception as ex:
                    pass

            if peticion == 'addmetodocalificacioncampo':
                try:
                    form = CampoDetalleMetodoCalificacionForm()
                    data['form'] = form
                    data['padre'] = request.GET['id']
                    data['peticion'] = 'addmetodocalificacioncampo'
                    template = get_template("configuraciones/modal/metodocalificacioncampo.html")
                    return JsonResponse({"respuesta": True, 'data': template.render(data)})
                except Exception as ex:
                    pass

            if peticion == 'crear_clase':
                try:
                    form = ClaseForm()
                    data['form'] = form
                    data['peticion'] = 'crear_clase'
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

            if peticion == 'editar_metodo_calificacion':
                try:
                    data['metodo'] = metodo = MetodoCalificacion.objects.get(pk=request.GET['id'])
                    form = MetodoCalifcacionForm(initial={
                        'nombre': metodo.nombre,
                        'nota_aprobacion': metodo.nota_aprobacion
                    })

                    data['form'] = form

                    data['peticion'] = 'editar_metodo_calificacion'
                    template = get_template("configuraciones/modal/metodocalificacion.html")
                    return JsonResponse({"respuesta": True, 'data': template.render(data)})
                except Exception as ex:
                    pass

            if peticion == 'editar_detalle_calificacion':
                try:
                    data['metodo'] = metodo = DetalleMetodoCalificacion.objects.get(pk=request.GET['id'])
                    form = DetalleMetodoCalificacionForm(initial={
                        'nombre': metodo.nombre,
                        'nota_aprobacion': metodo.nota_aprobacion
                    })
                    data['padre'] = request.GET['id']
                    data['form'] = form
                    data['peticion'] = 'editar_detalle_calificacion'
                    template = get_template("configuraciones/modal/metodocalificaciondetalle.html")
                    return JsonResponse({"respuesta": True, 'data': template.render(data)})
                except Exception as ex:
                    pass

            if peticion == 'editar_campo_calificacion':
                try:
                    data['metodo'] = metodo = CampoDetalleMetodoCalificacion.objects.get(pk=request.GET['id'])
                    form = CampoDetalleMetodoCalificacionForm(initial={
                        'nombre': metodo.nombre,
                        'nota_aprobacion': metodo.nota_aprobacion
                    })
                    data['padre'] = request.GET['id']
                    data['form'] = form

                    data['peticion'] = 'editar_campo_calificacion'
                    template = get_template("configuraciones/modal/metodocalificacioncampo.html")
                    return JsonResponse({"respuesta": True, 'data': template.render(data)})
                except Exception as ex:
                    pass



        else:
            try:
                data['titulo'] = 'Menú principal'
                return render(request, "configuraciones/view.html", data)
            except Exception as ex:
                print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno))
                pass
