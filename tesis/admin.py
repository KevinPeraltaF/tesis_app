from django.contrib import admin

# Register your models here.
from tesis.models import Clase, ClaseInscrita, Publicacion, MetodoCalificacion, DetalleMetodoCalificacion, \
    CampoDetalleMetodoCalificacion, DetallePublicacionVideo, DetallePublicacionMaterial, DetallePublicacionTarea, \
    tareaEstudiante


@admin.register(Clase)
class ClaseAdmin(admin.ModelAdmin):
    list_display = ('nombre','seccion','materia','aula','archivada','usuario_creacion','fecha_creacion','usuario_modificacion','fecha_modificacion','status',)
    search_fields = ('nombre','seccion','materia','aula',)


@admin.register(ClaseInscrita)
class ClaseInscritaAdmin(admin.ModelAdmin):
    list_display = ('usuario','clase','usuario_creacion','fecha_creacion','usuario_modificacion','fecha_modificacion','status',)
    search_fields = ('usuario','clase',)


admin.register(Publicacion)


class PublicacionAdmin(admin.ModelAdmin):
    list_display = (
    'clase', 'tipo_publicacion', 'titulo', 'instrucciones', 'clase', 'usuario_creacion', 'fecha_creacion',
    'usuario_modificacion', 'fecha_modificacion', 'status',)
    search_fields = ('titulo', 'instrucciones',)


@admin.register(Publicacion)
class PublicacionAdmin(admin.ModelAdmin):
    list_display = ('clase','tipo_publicacion','titulo','instrucciones','clase','usuario_creacion','fecha_creacion','usuario_modificacion','fecha_modificacion','status',)
    search_fields = ('titulo','instrucciones',)


@admin.register(MetodoCalificacion)
class MetodoCalificacionAdmin(admin.ModelAdmin):
    list_display = ('nombre','nota_aprobacion','usuario_creacion','fecha_creacion','usuario_modificacion','fecha_modificacion','status',)
    search_fields = ('nombre',)



@admin.register(DetalleMetodoCalificacion)
class DetalleMetodoCalificacionAdmin(admin.ModelAdmin):
    list_display = ('modelo','nombre','nota_aprobacion','usuario_creacion','fecha_creacion','usuario_modificacion','fecha_modificacion','status',)
    search_fields = ('nombre',)

@admin.register(CampoDetalleMetodoCalificacion)
class CampoDetalleMetodoCalificacionAdmin(admin.ModelAdmin):
    list_display = ('detallemetodocalificacion','nombre','nota_aprobacion','usuario_creacion','fecha_creacion','usuario_modificacion','fecha_modificacion','status',)
    search_fields = ('nombre',)


@admin.register(DetallePublicacionVideo)
class DetallePublicacionVideoAdmin(admin.ModelAdmin):
    list_display = ('publicacion','urlvideo','usuario_creacion','fecha_creacion','usuario_modificacion','fecha_modificacion','status',)
    search_fields = ('publicacion',)


@admin.register(DetallePublicacionMaterial)
class DetallePublicacionMaterialAdmin(admin.ModelAdmin):
    list_display = ('publicacion','archivo','usuario_creacion','fecha_creacion','usuario_modificacion','fecha_modificacion','status',)
    search_fields = ('publicacion',)



@admin.register(tareaEstudiante)
class tareaEstudianteAdmin(admin.ModelAdmin):
    list_display = ('tarea','estudiante','archivo','calificacion','fecha_de_entrega','calificado','estado_tarea','retroalimentacion','usuario_creacion','fecha_creacion','usuario_modificacion','fecha_modificacion','status',)
    search_fields = ('tarea',)


@admin.register(DetallePublicacionTarea)
class DetallePublicacionTareaAdmin(admin.ModelAdmin):
    list_display = ('publicacion','calificacion_maxima','fecha_fin_entrega','usuario_creacion','fecha_creacion','usuario_modificacion','fecha_modificacion','status',)
    search_fields = ('publicacion',)