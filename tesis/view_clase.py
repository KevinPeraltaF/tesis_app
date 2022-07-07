import sys
from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.db import transaction
from django.forms.models import model_to_dict
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.template.loader import get_template

from tesis.forms import CrearVideoForm, CrearMaterialForm, CrearTareaForm, SubirTareaForm, ClaseForm, UnirmeClaseForm, \
    MoverTareForm
from tesis.funciones import Data_inicial
from tesis.models import Clase, Publicacion, DetallePublicacionVideo, DetallePublicacionMaterial, \
    DetallePublicacionTarea, ClaseInscrita, tareaEstudiante, CampoDetalleMetodoCalificacion


@login_required(redirect_field_name='next', login_url='/login')
@transaction.atomic()
def Ver_Clase(request):
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

            if peticion == 'crear_tarea':
                try:
                    form = CrearTareaForm(request.POST, request.FILES)
                    id_clase = request.POST['id']
                    if form.is_valid():
                        titulo = form.cleaned_data['titulo']
                        instrucciones = form.cleaned_data['instrucciones']
                        fecha_fin_entrega = form.cleaned_data['fecha_fin_entrega']
                        ubicacionNota = form.cleaned_data['campo']
                        cabecera_publicacion = Publicacion(
                            clase_id=id_clase,
                            tipo_publicacion=1,
                            titulo=titulo,
                            instrucciones=instrucciones
                        )
                        cabecera_publicacion.save(request)
                        tarea = DetallePublicacionTarea(
                            publicacion=cabecera_publicacion,
                            calificacion_maxima=ubicacionNota.nota_aprobacion,
                            fecha_fin_entrega=fecha_fin_entrega,
                            campoubicacionNota = ubicacionNota
                        )
                        tarea.save(request)

                        return redirect("/clase/?peticion=ver_clase&id=%s" % id_clase)
                    else:
                        return redirect("/clase/?peticion=ver_clase&id=%s" % id_clase)


                except Exception as ex:
                    transaction.set_rollback(True)
                    return JsonResponse({"respuesta": False, "mensaje": "Ha ocurrido un error, intente mas tarde."})
            if peticion == 'mover_tarea':
                try:
                    form = MoverTareForm(request.POST, request.FILES)
                    id_Tarea = request.POST['id']
                    tarea = DetallePublicacionTarea.objects.get(pk=id_Tarea)

                    if form.is_valid():
                        ubicacionNota = form.cleaned_data['campo']

                        tarea.campoubicacionNota = ubicacionNota
                        tarea.save(request)

                        return redirect("/clase/?peticion=ver_clase&id=%s" % tarea.publicacion.clase.pk)
                    else:
                        return redirect("/clase/?peticion=ver_clase&id=%s" % tarea.publicacion.clase.pk)


                except Exception as ex:
                    transaction.set_rollback(True)
                    return JsonResponse({"respuesta": False, "mensaje": "Ha ocurrido un error, intente mas tarde."})

            if peticion == 'editar_tarea':
                try:
                    form = CrearTareaForm(request.POST, request.FILES)
                    publicacion = Publicacion.objects.get(pk=request.POST['id_publicacion'])
                    tarea = DetallePublicacionTarea.objects.get(publicacion=request.POST['id_publicacion'])
                    if form.is_valid():
                        titulo = form.cleaned_data['titulo']
                        instrucciones = form.cleaned_data['instrucciones']
                        calificacion_maxima = form.cleaned_data['calificacion_maxima']
                        fecha_fin_entrega = form.cleaned_data['fecha_fin_entrega']

                        publicacion.titulo = titulo
                        publicacion.instrucciones = instrucciones
                        publicacion.save(request)

                        tarea.calificacion_maxima = calificacion_maxima
                        tarea.fecha_fin_entrega = fecha_fin_entrega
                        tarea.save(request)

                        return redirect("/clase/?peticion=ver_clase&id=%s" % publicacion.clase.pk)
                    else:
                        return redirect("/clase/?peticion=ver_clase&id=%s" % publicacion.clase.pk)


                except Exception as ex:
                    transaction.set_rollback(True)
                    return JsonResponse({"respuesta": False, "mensaje": "Ha ocurrido un error, intente mas tarde."})

            if peticion == 'crear_material':
                try:
                    form = CrearMaterialForm(request.POST, request.FILES)
                    id_clase = request.POST['id']
                    if form.is_valid():
                        titulo = form.cleaned_data['titulo']
                        instrucciones = form.cleaned_data['instrucciones']
                        archivo = form.cleaned_data['archivo']

                        cabecera_publicacion = Publicacion(
                            clase_id=id_clase,
                            tipo_publicacion=2,
                            titulo=titulo,
                            instrucciones=instrucciones
                        )
                        cabecera_publicacion.save(request)

                        detalle_material = DetallePublicacionMaterial(
                            publicacion=cabecera_publicacion,
                            archivo=archivo
                        )

                        detalle_material.save(request)

                        return redirect("/clase/?peticion=ver_clase&id=%s" % id_clase)
                    else:
                        return redirect("/clase/?peticion=ver_clase&id=%s" % id_clase)


                except Exception as ex:
                    transaction.set_rollback(True)
                    return JsonResponse({"respuesta": False, "mensaje": "Ha ocurrido un error, intente mas tarde."})

            if peticion == 'editar_material':
                try:
                    form = CrearMaterialForm(request.POST, request.FILES)
                    publicacion = Publicacion.objects.get(pk=request.POST['id_publicacion'])
                    if form.is_valid():
                        titulo = form.cleaned_data['titulo']
                        instrucciones = form.cleaned_data['instrucciones']
                        archivo = form.cleaned_data['archivo']

                        publicacion.titulo = titulo
                        publicacion.instrucciones = instrucciones
                        publicacion.save(request)

                        material = DetallePublicacionMaterial.objects.get(publicacion=publicacion)
                        material.archivo = archivo
                        material.save()

                        return redirect("/clase/?peticion=ver_clase&id=%s" % publicacion.clase.pk)
                    else:
                        return redirect("/clase/?peticion=ver_clase&id=%s" % publicacion.clase.pk)


                except Exception as ex:
                    transaction.set_rollback(True)
                    return JsonResponse({"respuesta": False, "mensaje": "Ha ocurrido un error, intente mas tarde."})

            if peticion == 'crear_video':
                try:
                    form = CrearVideoForm(request.POST, request.FILES)
                    id_clase = request.POST['id']
                    if form.is_valid():
                        titulo = form.cleaned_data['titulo']
                        instrucciones = form.cleaned_data['instrucciones']
                        urlvideo = form.cleaned_data['urlvideo']

                        cabecera_publicacion = Publicacion(
                            clase_id=id_clase,
                            tipo_publicacion=3,
                            titulo=titulo,
                            instrucciones=instrucciones
                        )
                        cabecera_publicacion.save(request)

                        detalle_video = DetallePublicacionVideo(
                            publicacion=cabecera_publicacion,
                            urlvideo=urlvideo
                        )

                        detalle_video.save(request)

                        return redirect("/clase/?peticion=ver_clase&id=%s" % id_clase)
                    else:
                        return redirect("/clase/?peticion=ver_clase&id=%s" % id_clase)


                except Exception as ex:
                    transaction.set_rollback(True)
                    return JsonResponse({"respuesta": False, "mensaje": "Ha ocurrido un error, intente mas tarde."})

            if peticion == 'editar_video':
                try:
                    form = CrearVideoForm(request.POST, request.FILES)
                    publicacion = Publicacion.objects.get(pk=request.POST['id_publicacion'])
                    if form.is_valid():
                        titulo = form.cleaned_data['titulo']
                        instrucciones = form.cleaned_data['instrucciones']
                        urlvideo = form.cleaned_data['urlvideo']

                        publicacion.titulo = titulo
                        publicacion.instrucciones = instrucciones
                        publicacion.save(request)

                        video = DetallePublicacionVideo.objects.get(publicacion=publicacion)
                        video.urlvideo = urlvideo
                        video.save()

                        return redirect("/clase/?peticion=ver_clase&id=%s" % publicacion.clase.pk)
                    else:
                        return redirect("/clase/?peticion=ver_clase&id=%s" % publicacion.clase.pk)


                except Exception as ex:
                    transaction.set_rollback(True)
                    return JsonResponse({"respuesta": False, "mensaje": "Ha ocurrido un error, intente mas tarde."})

            if peticion == 'actualizar_codigo_clase':
                try:
                    with transaction.atomic():
                        registro = Clase.objects.get(pk=request.POST['id'])
                        generador_codigo_clase = User.objects.make_random_password(length=7)
                        while Clase.objects.filter(codigo_clase=generador_codigo_clase).exists():
                            generador_codigo_clase = User.objects.make_random_password(length=7)
                        registro.codigo_clase = generador_codigo_clase
                        registro.save(request)
                        return JsonResponse(
                            {"respuesta": True, "mensaje": "Código de clase actualizado correctamente."})

                except Exception as ex:
                    pass

            if peticion == 'eliminar_publicacion':
                try:
                    with transaction.atomic():
                        registro = Publicacion.objects.get(pk=request.POST['id'])
                        registro.status = False
                        registro.save(request)
                        return JsonResponse({"respuesta": True, "mensaje": "Registro eliminado correctamente."})

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

            if peticion == 'subir_tarea':
                try:
                    form = SubirTareaForm(request.POST, request.FILES)
                    if form.is_valid():
                        archivo = form.cleaned_data['archivo']
                        id_tarea = request.POST['id']

                        if tareaEstudiante.objects.filter(status=True, tarea_id=id_tarea,
                                                          estudiante_id=request.user).exists():
                            subir_tarea = tareaEstudiante.objects.get(status=True, tarea_id=id_tarea,estudiante=request.user)
                            subir_tarea.archivo = archivo
                            subir_tarea.save(request)

                        else:
                            subir_tarea = tareaEstudiante(
                                tarea_id=id_tarea,
                                estudiante=request.user,
                                archivo=archivo,
                                fecha_de_entrega=datetime.now().date(),
                                estado_tarea=2

                            )
                            subir_tarea.save(request)

                        return redirect("/clase/?peticion=ver_tarea&clase_id=%s&tarea_id=%s" % (
                            subir_tarea.tarea.publicacion.clase.id, subir_tarea.tarea.publicacion.pk))


                    else:
                        return redirect("/")


                except Exception as ex:
                    transaction.set_rollback(True)
                    return JsonResponse({"respuesta": False, "mensaje": "Ha ocurrido un error, intente mas tarde."})

            if peticion == 'ingresar_calificacion':
                try:
                    tarea = tareaEstudiante.objects.get(id=int(request.POST['id']))
                    tarea.calificacion = request.POST['calificacion']
                    tarea.calificado =True
                    tarea.estado_tarea = 1
                    tarea.save(request)
                    return JsonResponse({"respuesta": True, "mensaje": "calificación guardada correctamente."})
                except Exception as ex:
                    pass

            if peticion == 'ingresar_observacion':
                try:
                    tarea = tareaEstudiante.objects.get(id=int(request.POST['id']))
                    tarea.retroalimentacion = request.POST['observacion']
                    tarea.save(request)
                    return JsonResponse({"respuesta": True, "mensaje": "calificación guardada correctamente."})
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

            if peticion == 'unirme_a_clase':
                try:
                    form = UnirmeClaseForm()
                    data['form'] = form
                    data['peticion'] = 'unirme_a_clase'
                    template = get_template("clase/formUnirmeClase.html")
                    return JsonResponse({"respuesta": True, 'data': template.render(data)})
                except Exception as ex:
                    pass

            if peticion == 'cursos_inscritos':
                try:
                    data['peticion'] = 'cursos_inscritos'
                    usuariio = request.user
                    data['cursos_inscritos'] = cursos_inscritos = ClaseInscrita.objects.filter(status=True,
                                                                                               usuario=usuariio)
                    return render(request, "clase/clases_inscritas.html", data)
                except Exception as ex:
                    print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno))
                    pass

            if peticion == 'clases_archivadas':
                try:
                    data['peticion'] = 'clases_archivadas'
                    data['clases_archivadas'] = clases_archivadas = Clase.objects.filter(status=True, archivada=True,
                                                                                         usuario_creacion=request.user)
                    return render(request, "clase/clases_Archivadas.html", data)
                except Exception as ex:
                    print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno))
                    pass

            if peticion == 'ver_clase':
                try:
                    data['mi_clase'] = clase = Clase.objects.get(pk=request.GET['id'])
                    publicacion = Publicacion.objects.filter(status=True, clase=clase).exclude(
                        tipo_publicacion=1).order_by(
                        '-id')

                    publicacionpanel = Publicacion.objects.filter(status=True, clase=clase).order_by(
                        '-id')
                    data['tarea'] = tarea = Publicacion.objects.filter(status=True, clase=clase,
                                                                       tipo_publicacion=1).order_by('-id')
                    data['metodo'] = clase.modelo
                    data['detalle'] = clase.modelo.obtenerDetallemetododetallecalificacion()

                    paginator = Paginator(publicacionpanel, 15)
                    page_number = request.GET.get('page')
                    page_obj = paginator.get_page(page_number)
                    data['publicacionpanel'] = page_obj

                    paginator2 = Paginator(publicacion, 15)
                    page_number2 = request.GET.get('page2')
                    page_obj2 = paginator2.get_page(page_number2)
                    data['publicacion'] = page_obj2

                    inscritos = clase.obtener_inscritos()

                    paginator3 = Paginator(inscritos, 15)
                    page_number3 = request.GET.get('page3')
                    page_obj3 = paginator3.get_page(page_number3)
                    data['inscritos'] = page_obj3

                    return render(request, "clase/clase.html", data)
                except Exception as ex:
                    pass

            if peticion == 'ver_tareas_entregadas':
                try:
                    data['tarea'] = tarea = DetallePublicacionTarea.objects.get(publicacion_id=request.GET['id'])

                    return render(request, "clase/profesor/tareas_entregadas.html", data)
                except Exception as ex:
                    pass

            if peticion == 'estudiante_ver_clase':
                try:
                    data['curso'] = curso = Clase.objects.get(pk=request.GET['id'])
                    data['publicacion'] = publicacion = Publicacion.objects.filter(status=True, clase=curso).order_by(
                        '-id')
                    data['publicacion_tipo_tarea'] = publicacion_tipo_tarea = Publicacion.objects.filter(status=True,
                                                                                                         clase=curso,
                                                                                                         tipo_publicacion=1).order_by(
                        '-id')

                    data['metodo'] = curso.modelo
                    data['detalle'] = curso.modelo.obtenerDetallemetododetallecalificacion()
                    return render(request, "clase/estudiante/estudiante_ver_clase.html", data)
                except Exception as ex:
                    pass

            if peticion == 'ver_tarea':
                try:
                    clase_id = request.GET['clase_id']
                    tarea_id = request.GET['tarea_id']
                    data['curso'] = Clase.objects.get(pk=clase_id)
                    data['tarea'] = publicac = Publicacion.objects.get(pk=tarea_id)
                    if publicac.obtener_tarea().tiene_tarea(request.user):
                        data['estado_entrega'] = publicac.obtener_tarea().obtener_tarea_de_estudiante(request.user)
                    else:
                        data['estado_entrega'] = None
                    return render(request, "clase/estudiante/ver_tarea_estudiante.html", data)
                except Exception as ex:
                    print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno))
                    pass

            if peticion == 'ver_video':
                try:
                    clase_id = request.GET['clase_id']
                    video_id = request.GET['video_id']
                    data['curso'] = Clase.objects.get(pk=clase_id)
                    data['video'] = Publicacion.objects.get(pk=video_id)

                    return render(request, "clase/estudiante/ver_video_estudiante.html", data)
                except Exception as ex:
                    print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno))
                    pass

            if peticion == 'ver_material':
                try:
                    clase_id = request.GET['clase_id']
                    material_id = request.GET['material_id']
                    data['curso'] = Clase.objects.get(pk=clase_id)
                    data['material'] = Publicacion.objects.get(pk=material_id)

                    return render(request, "clase/estudiante/ver_material_estudiante.html", data)
                except Exception as ex:
                    print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno))
                    pass

            if peticion == 'crear_tarea':
                try:
                    form = CrearTareaForm()
                    data['form'] = form
                    modelo = Clase.objects.get(pk=request.GET['id'])
                    form.add(modelo.modelo)
                    data['peticion'] = 'crear_tarea'
                    data['id_clase'] = request.GET['id']
                    template = get_template("clase/profesor/formCrearTarea.html")
                    return JsonResponse({"respuesta": True, 'data': template.render(data)})
                except Exception as ex:
                    pass

            if peticion == 'editar_tarea':
                try:
                    data['publicacion'] = publicacion = Publicacion.objects.get(pk=request.GET['id'])
                    form = CrearTareaForm(initial={
                        'titulo': publicacion.titulo,
                        'instrucciones': publicacion.instrucciones,
                        'calificacion_maxima': publicacion.obtener_tarea().calificacion_maxima,
                        'fecha_fin_entrega': publicacion.obtener_tarea().fecha_fin_entrega,
                        'metodo': publicacion.obtener_tarea().campoubicacionNota.detallemetodocalificacion.modelo,
                        'detallecalificacion': publicacion.obtener_tarea().campoubicacionNota.detallemetodocalificacion,
                        'campo': publicacion.obtener_tarea().campoubicacionNota
                    })
                    form.edit(publicacion.obtener_tarea().campoubicacionNota.detallemetodocalificacion.modelo,publicacion.obtener_tarea().campoubicacionNota.detallemetodocalificacion,publicacion.obtener_tarea().campoubicacionNota)
                    data['form'] = form
                    data['id_clase'] = request.GET['id']
                    data['peticion'] = 'editar_tarea'
                    template = get_template("clase/profesor/formCrearTarea.html")
                    return JsonResponse({"respuesta": True, 'data': template.render(data)})
                except Exception as ex:
                    pass


            if peticion == 'mover_tarea':
                try:
                    form = MoverTareForm()
                    Tarea = DetallePublicacionTarea.objects.get(pk=request.GET['id'])
                    modelo = Tarea.campoubicacionNota.detallemetodocalificacion.modelo
                    detalle = Tarea.campoubicacionNota.detallemetodocalificacion
                    campo = Tarea.campoubicacionNota
                    form.add(modelo,detalle,campo)
                    data['form'] = form
                    data['peticion'] = 'mover_tarea'
                    data['tarea'] = Tarea
                    template = get_template("clase/profesor/form_mover_tarea.html")
                    return JsonResponse({"respuesta": True, 'data': template.render(data)})
                except Exception as ex:
                    pass

            if peticion == 'crear_video':
                try:
                    form = CrearVideoForm()
                    data['form'] = form
                    data['peticion'] = 'crear_video'
                    data['id_clase'] = request.GET['id']
                    template = get_template("clase/profesor/formCrearVideo.html")
                    return JsonResponse({"respuesta": True, 'data': template.render(data)})
                except Exception as ex:
                    pass

            if peticion == 'editar_video':
                try:
                    data['publicacion'] = publicacion = Publicacion.objects.get(pk=request.GET['id'])

                    form = CrearVideoForm(initial={
                        'titulo': publicacion.titulo,
                        'instrucciones': publicacion.instrucciones,
                        'urlvideo': publicacion.obtener_detalle_video().urlvideo,

                    })
                    data['form'] = form
                    data['id_clase'] = request.GET['id']
                    data['peticion'] = 'editar_video'
                    template = get_template("clase/profesor/formCrearTarea.html")
                    return JsonResponse({"respuesta": True, 'data': template.render(data)})
                except Exception as ex:
                    pass

            if peticion == 'crear_material':
                try:
                    form = CrearMaterialForm()
                    data['form'] = form
                    data['peticion'] = 'crear_material'
                    data['id_clase'] = request.GET['id']
                    template = get_template("clase/profesor/formCrearMaterial.html")
                    return JsonResponse({"respuesta": True, 'data': template.render(data)})
                except Exception as ex:
                    pass

            if peticion == 'editar_material':
                try:
                    data['publicacion'] = publicacion = Publicacion.objects.get(pk=request.GET['id'])

                    form = CrearMaterialForm(initial={
                        'titulo': publicacion.titulo,
                        'instrucciones': publicacion.instrucciones,
                        'archivo': publicacion.obtener_detalle_material().archivo,

                    })
                    data['form'] = form
                    data['id_clase'] = request.GET['id']
                    data['peticion'] = 'editar_tarea'
                    template = get_template("clase/profesor/formCrearTarea.html")
                    return JsonResponse({"respuesta": True, 'data': template.render(data)})
                except Exception as ex:
                    pass

            if peticion == 'subir_tarea':
                try:
                    form = SubirTareaForm()
                    data['form'] = form
                    data['peticion'] = 'subir_tarea'
                    data['id_tarea'] = request.GET['id']
                    template = get_template("clase/estudiante/formSubirTarea.html")
                    return JsonResponse({"respuesta": True, 'data': template.render(data)})
                except Exception as ex:
                    pass

            if peticion == 'cargar_campo_calificacion':
                try:
                    lista = []
                    campos = CampoDetalleMetodoCalificacion.objects.filter(
                        detallemetodocalificacion_id=int(request.GET['id']), status=True)
                    for campo in campos:
                        lista.append([campo.id, campo.nombre])

                    return JsonResponse({"respuesta": True, 'lista': lista})
                except Exception as ex:
                    pass


        else:
            try:
                data['titulo'] = 'Menú principal'
                return render(request, "clase/clase.html", data)
            except Exception as ex:
                print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno))
                pass
