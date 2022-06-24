import os
from datetime import datetime

from django.contrib.auth.models import User
from django.db import models


# Create your models here.
from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver

from tesis_app import settings
TIPO_PUBLICACION = (
    (1, u"TAREA"),
    (2, u"MATERIAL"),
    (3, u"VIDEO"),
)

class ModeloBase(models.Model):
    from django.contrib.auth.models import User
    usuario_creacion = models.ForeignKey(User, verbose_name='Usuario Creación', blank=True, null=True,
                                         on_delete=models.CASCADE, related_name='+', editable=False)
    fecha_creacion = models.DateTimeField(verbose_name='Fecha creación', auto_now_add=True)
    fecha_modificacion = models.DateTimeField(verbose_name='Fecha Modificación', auto_now=True)
    usuario_modificacion = models.ForeignKey(User, verbose_name='Usuario Modificación', blank=True, null=True,
                                             on_delete=models.CASCADE, related_name='+', editable=False)
    status = models.BooleanField(verbose_name="Estado del registro", default=True)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        usuario = None
        if len(args):
            usuario = args[0].user.id
        if self.id:
            self.usuario_modificacion_id = usuario
        else:
            self.usuario_creacion_id = usuario
        models.Model.save(self)


class Clase(ModeloBase):
    nombre = models.CharField(verbose_name="Nombre de la clase", max_length=100)
    seccion = models.CharField(verbose_name="Sección", max_length=100)
    materia = models.CharField(verbose_name="Materia", max_length=100)
    aula = models.CharField(verbose_name="Aula", max_length=100)
    archivada = models.BooleanField(default=False, verbose_name=u'Archivada')
    codigo_clase = models.CharField(verbose_name="Código de la clase", max_length=100, null=True, unique=True)

    class Meta:
        verbose_name = "Clase"
        verbose_name_plural = "Clases"
        ordering = ['id']

    def __str__(self):
        return u'%s' % self.nombre

    def obtener_inscritos(self):
        return self.claseinscrita_set.filter(status=True)

    def obtener_profesor_clase(self):
        if Persona.objects.filter(usuario=self.usuario_creacion, status=True).exists():
            persona = Persona.objects.get(usuario=self.usuario_creacion, status=True)
        else:
            persona = self.usuario_creacion
        return persona


class Persona(ModeloBase):
    usuario = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    nombre1 = models.CharField(max_length=100, verbose_name='1er Nombre')
    nombre2 = models.CharField(max_length=100, verbose_name='2do Nombre')
    apellido1 = models.CharField(max_length=100, verbose_name="1er Apellido")
    apellido2 = models.CharField(max_length=100, verbose_name="2do Apellido")
    email = models.CharField(default='', max_length=200, verbose_name="Correo electronico")

    class Meta:
        verbose_name = "Persona"
        verbose_name_plural = "Personas"
        ordering = ['id']

    def __str__(self):
        return u'%s %s %s %s' % (self.apellido1, self.apellido2, self.nombre1, self.nombre2)


class ClaseInscrita(ModeloBase):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    clase = models.ForeignKey(Clase, on_delete=models.CASCADE)

    def __str__(self):
        if Persona.objects.filter(usuario=self.usuario, status=True).exists():
            persona = Persona.objects.get(usuario=self.usuario, status=True)
        else:
            persona = self.usuario
        return u'%s' % persona

    def obtener_profesor(self):
        if Persona.objects.filter(usuario=self.clase.usuario_creacion, status=True).exists():
            persona = Persona.objects.get(usuario=self.clase.usuario_creacion, status=True)
        else:
            persona = self.clase.usuario_creacion
        return persona




class Publicacion(ModeloBase):
    clase = models.ForeignKey(Clase, null=True, on_delete=models.CASCADE)
    tipo_publicacion = models.IntegerField(choices=TIPO_PUBLICACION, null=True, blank=True,
                                           verbose_name='Tipo publicación')
    titulo = models.CharField(max_length=100, verbose_name="Titulo")
    instrucciones = models.CharField(max_length=100, verbose_name=u"Instrucciones")

    def __str__(self):
        return u'%s - %s' % (self.get_tipo_publicacion_display(), self.titulo)

    def obtener_detalle_material(self):
        return self.detallepublicacionmaterial_set.filter(status=True)[0]

    def obtener_detalle_video(self):
        return self.detallepublicacionvideo_set.filter(status=True)[0]

    def obtener_tarea(self):
        return self.detallepublicaciontarea_set.get()








ESTADO_TAREA = (
    (1, "CALIFICADO"),
    (2, "ENVIADO PARA CALIFICAR"),
    (3, "NO ENTREGADO"),
)
class DetallePublicacionTarea(ModeloBase):
    publicacion = models.ForeignKey(Publicacion, null=True, on_delete=models.CASCADE)
    calificacion_maxima = models.IntegerField(verbose_name="Calificación máxima", blank=True, null=True)
    fecha_fin_entrega = models.DateField(verbose_name='Fecha máxima de entrega', blank=True, null=True)

    def __str__(self):
        return '%s' % self.publicacion

    def puede_subir_tarea(self):
        if self.fecha_fin_entrega > datetime.now().date():
            return False
        else:
            return True

    def obtener_tarea_de_estudiante(self, usuario):
        return self.tareaestudiante_set.get(status=True,estudiante = usuario)

    def tiene_tarea(self,usuario):
        return self.tareaestudiante_set.filter(status=True,estudiante = usuario).exists()

    def obtener_total_calificados(self):
        return tareaEstudiante.objects.filter(status=True, tarea=self, calificado=True).count()

    def obtener_total_inscritos(self):
        return ClaseInscrita.objects.filter(status=True,clase =self.publicacion.clase).count()

    def obtener_total_entregados(self):
        return tareaEstudiante.objects.filter(status=True,tarea = self).count()

    def obtener_inscritos_entregados(self):
        return tareaEstudiante.objects.filter(status=True, tarea=self)

    def obtener_inscritos_no_entregados(self):
        estudiantes_si_entregaron = tareaEstudiante.objects.values_list('estudiante').filter(status=True, tarea=self)
        return ClaseInscrita.objects.filter(status=True,clase=self.publicacion.clase).exclude(usuario__in=estudiantes_si_entregaron)

class tareaEstudiante(ModeloBase):
    tarea =  models.ForeignKey(DetallePublicacionTarea, null=True, on_delete=models.CASCADE)
    estudiante = models.ForeignKey(User, on_delete=models.CASCADE)
    archivo = models.FileField(upload_to='tareas_Estudiantes/%Y/%m/%d', blank=True, null=True,
                               verbose_name='Archivo Tarea')
    calificacion = models.IntegerField(verbose_name="Calificación", blank=True, null=True)
    fecha_de_entrega = models.DateTimeField(verbose_name='Fecha de entrega', blank=True, null=True)
    calificado = models.BooleanField(verbose_name="Estado calificado", default=False)
    estado_tarea = models.IntegerField(choices=ESTADO_TAREA, null=True, blank=True, verbose_name='Tipo publicación')
    retroalimentacion = models.TextField(default='', verbose_name='Retroalimentacion', blank=True, null=True)


    def __str__(self):
        if self.calificado:
            estado_calificacion = 'Calificado'
        else:
            estado_calificacion = 'No calificado'

        if self.calificado:
            estado_entrega = 'Entregado'
        else:
            estado_entrega = 'No entregado'

        return u'%s - %s - %s' % (self.tarea, estado_entrega, estado_calificacion)

    def obtener_estudiante(self):
        if Persona.objects.filter(usuario=self.estudiante, status=True).exists():
            persona = Persona.objects.get(usuario=self.estudiante, status=True)
        else:
            persona = self.estudiante
        return persona

class DetallePublicacionMaterial(ModeloBase):
    publicacion = models.ForeignKey(Publicacion, null=True, on_delete=models.CASCADE)
    archivo = models.FileField(upload_to='material_subido/%Y/%m/%d', verbose_name='Archivo Material')

    def __str__(self):
        return u'%s - %s' % (self.publicacion, self.get_tipo_archivo_display())



class DetallePublicacionVideo(ModeloBase):
    publicacion = models.ForeignKey(Publicacion, null=True, on_delete=models.CASCADE)
    urlvideo = models.TextField(default='', verbose_name=u'URL Video')

    def __str__(self):
        return u'%s - %s' % (self.publicacion, self.urlvideo)





@receiver(post_delete, sender=DetallePublicacionMaterial)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """
    Deletes file from filesystem
    when corresponding `MediaFile` object is deleted.
    """
    ruta = settings.MEDIA_ROOT +"\\"+ str(instance.archivo)
    if ruta:
        if os.path.isfile(ruta):
            os.remove(ruta)
@receiver(pre_save, sender=DetallePublicacionMaterial)
def auto_delete_file_on_change(sender, instance, **kwargs):
    """
    Deletes old file from filesystem
    when corresponding `MediaFile` object is updated
    with new file.
    """
    if not instance.pk:
        return False

    try:
        old_file = DetallePublicacionMaterial.objects.get(pk=instance.pk).archivo
    except DetallePublicacionMaterial.DoesNotExist:
        return False

    new_file = instance.archivo
    if not old_file == new_file:
        ruta = settings.MEDIA_ROOT +"\\"+ str(old_file)
        if os.path.isfile(ruta):
            os.remove(ruta)


