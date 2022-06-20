from django.contrib import admin

# Register your models here.
from tesis.models import Clase, ClaseInscrita, Publicacion


@admin.register(Clase)
class ClaseAdmin(admin.ModelAdmin):
    list_display = ('nombre','seccion','materia','aula','archivada','usuario_creacion','fecha_creacion','usuario_modificacion','fecha_modificacion','status',)
    search_fields = ('nombre','seccion','materia','aula',)


@admin.register(ClaseInscrita)
class ClaseInscritaAdmin(admin.ModelAdmin):
    list_display = ('usuario','clase','usuario_creacion','fecha_creacion','usuario_modificacion','fecha_modificacion','status',)
    search_fields = ('usuario','clase',)



@admin.register(Publicacion)
class PublicacionAdmin(admin.ModelAdmin):
    list_display = ('clase','tipo_publicacion','titulo','instrucciones','calificacion_maxima','fecha_fin_entrega','clase','usuario_creacion','fecha_creacion','usuario_modificacion','fecha_modificacion','status',)
    search_fields = ('titulo','instrucciones',)