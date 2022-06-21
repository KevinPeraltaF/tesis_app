import sys

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db import transaction
from django.forms.models import model_to_dict
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.template.loader import get_template

from tesis.forms import CrearVideoForm, CrearMaterialForm, CrearTareaForm
from tesis.funciones import Data_inicial
from tesis.models import Clase, Publicacion, DetallePublicacionVideo, DetallePublicacionMaterial, \
    DetallePublicacionTarea, ClaseInscrita


@login_required(redirect_field_name='next', login_url='/login')
@transaction.atomic()
def Ver_Clase(request):
    global ex
    data = {}
    Data_inicial(request, data)
    if request.method == 'POST':
        if 'peticion' in request.POST:
            peticion = request.POST['peticion']

            if peticion == 'crear_tarea':
                try:
                    form = CrearTareaForm(request.POST, request.FILES)
                    id_clase = request.POST['id']
                    if form.is_valid():
                        titulo = form.cleaned_data['titulo']
                        instrucciones = form.cleaned_data['instrucciones']
                        calificacion_maxima = form.cleaned_data['calificacion_maxima']
                        fecha_fin_entrega = form.cleaned_data['fecha_fin_entrega']

                        cabecera_publicacion = Publicacion(
                            clase_id=id_clase,
                            tipo_publicacion=1,
                            titulo=titulo,
                            instrucciones=instrucciones,
                            calificacion_maxima=calificacion_maxima,
                            fecha_fin_entrega=fecha_fin_entrega
                        )
                        cabecera_publicacion.save(request)

                        estudiantes_de_la_clase = ClaseInscrita.objects.filter(status=True, clase__id=id_clase)
                        for estudiante in estudiantes_de_la_clase:
                            detalle_tarea = DetallePublicacionTarea(
                                publicacion=cabecera_publicacion,
                                estudiante=estudiante.usuario,
                                archivo=None,
                                calificacion=None,
                                fecha_de_entrega=None,
                                retroalimentacion=None

                            )
                            detalle_tarea.save(request)

                        return redirect("/clase/?peticion=ver_clase&id=%s" % id_clase)
                    else:
                        return redirect("/clase/?peticion=ver_clase&id=%s" % id_clase)


                except Exception as ex:
                    transaction.set_rollback(True)
                    return JsonResponse({"respuesta": False, "mensaje": "Ha ocurrido un error, intente mas tarde."})

            if peticion == 'editar_tarea':
                try:
                    form = CrearTareaForm(request.POST, request.FILES)
                    publicacion = Publicacion.objects.get(pk=request.POST['id_publicacion'])
                    if form.is_valid():
                        titulo = form.cleaned_data['titulo']
                        instrucciones = form.cleaned_data['instrucciones']
                        calificacion_maxima = form.cleaned_data['calificacion_maxima']
                        fecha_fin_entrega = form.cleaned_data['fecha_fin_entrega']

                        publicacion.titulo = titulo
                        publicacion.instrucciones = instrucciones
                        publicacion.calificacion_maxima = calificacion_maxima
                        publicacion.fecha_fin_entrega = fecha_fin_entrega

                        publicacion.save(request)

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

    else:
        if 'peticion' in request.GET:
            peticion = request.GET['peticion']

            if peticion == 'cursos_inscritos':
                try:
                    data['peticion'] = 'cursos_inscritos'
                    usuariio = request.user
                    data['cursos_inscritos'] = cursos_inscritos = ClaseInscrita.objects.filter(status=True,
                                                                                               usuario=usuariio)
                    return render(request, "clase/clases_inscritas.html ", data)
                except Exception as ex:
                    print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno))

            if peticion == 'clases_archivadas':
                try:
                    data['peticion'] = 'clases_archivadas'
                    data['clases_archivadas'] = clases_archivadas = Clase.objects.filter(status=True, archivada=True,
                                                                                         usuario_creacion=request.user)
                    return render(request, "clase/clases_Archivadas.html ", data)
                except Exception as ex:
                    print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno))

            if peticion == 'ver_clase':
                try:
                    data['mi_clase'] = clase = Clase.objects.get(pk=request.GET['id'])
                    data['publicacion'] = publicacion = Publicacion.objects.filter(status=True, clase=clase).order_by(
                        '-id')
                    return render(request, "clase/clase.html", data)
                except Exception as ex:
                    pass

            if peticion == 'estudiante_ver_clase':
                try:
                    data['curso'] = curso = Clase.objects.get(pk=request.GET['id'])
                    data['publicacion'] = publicacion = Publicacion.objects.filter(status=True, clase=curso).order_by('-id')
                    return render(request, "clase/estudiante/estudiante_ver_clase.html", data)
                except Exception as ex:
                    pass


            if peticion == 'crear_tarea':
                try:
                    form = CrearTareaForm()
                    data['form'] = form
                    data['peticion'] = 'crear_tarea'
                    data['id_clase'] = request.GET['id']
                    template = get_template("clase/profesor/formCrearTarea.html")
                    return JsonResponse({"respuesta": True, 'data': template.render(data)})
                except Exception as ex:
                    pass

            if peticion == 'editar_tarea':
                try:
                    data['publicacion'] = publicacion = Publicacion.objects.get(pk=request.GET['id'])
                    form = CrearTareaForm(initial=model_to_dict(publicacion))
                    data['form'] = form
                    data['id_clase'] = request.GET['id']
                    data['peticion'] = 'editar_tarea'
                    template = get_template("clase/profesor/formCrearTarea.html")
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
                    data['peticion'] = 'editar_tarea'
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


        else:
            try:
                data['titulo'] = 'Menú principal'
                return render(request, "clase/clase.html ", data)
            except Exception as ex:
                print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno))
