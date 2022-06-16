from django.contrib import admin

# Register your models here.
from tesis.models import Clase


@admin.register(Clase)
class ClaseAdmin(admin.ModelAdmin):
    list_display = ('nombre','seccion','materia','aula','archivada','usuario_creacion','fecha_creacion','usuario_modificacion','fecha_modificacion','status',)
    search_fields = ('nombre','seccion','materia','aula',)