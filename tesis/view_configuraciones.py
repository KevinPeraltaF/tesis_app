import sys
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.template.loader import get_template

from tesis.forms import MetodoCalifcacionForm, DetalleMetodoCalificacionForm, CampoDetalleMetodoCalificacionForm
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
                    data['padre'] = request.GET['id']
                    return render(request, "configuraciones/detalle.html", data)
                except Exception as ex:
                    pass

            if peticion == 'agregar_campo_detalle_modelo':
                try:
                    campo = CampoDetalleMetodoCalificacion.objects.filter(detallemetodocalificacion_id=request.GET['id'],status=True)
                    data['campo'] = campo
                    data['padre'] = request.GET['id']
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

        else:
            try:
                data['titulo'] = 'Menú principal'
                return render(request, "configuraciones/view.html", data)
            except Exception as ex:
                print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno))
                pass
