from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class ModeloBase(models.Model):
    from django.contrib.auth.models import User
    usuario_creacion = models.ForeignKey(User, verbose_name='Usuario Creación', blank=True, null=True, on_delete= models.CASCADE, related_name='+', editable=False)
    fecha_creacion = models.DateTimeField(verbose_name='Fecha creación',auto_now_add=True)
    fecha_modificacion = models.DateTimeField(verbose_name='Fecha Modificación', auto_now=True)
    usuario_modificacion = models.ForeignKey(User, verbose_name='Usuario Modificación', blank=True, null=True, on_delete= models.CASCADE, related_name='+', editable=False)
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
    seccion =models.CharField(verbose_name="Sección", max_length=100)
    materia =models.CharField(verbose_name="Materia", max_length=100)
    aula =models.CharField(verbose_name="Aula", max_length=100)
    archivada = models.BooleanField(default=False, verbose_name=u'Archivada')
    codigo_clase = models.CharField(verbose_name="Código de la clase", max_length=100,null=True , unique=True)
    class Meta:
        verbose_name = "Clase"
        verbose_name_plural = "Clases"
        ordering = ['id']


    def __str__(self):
        return u'%s' % self.nombre


class Persona(ModeloBase):
    usuario = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    nombre1 = models.CharField(max_length=100, verbose_name=u'1er Nombre')
    nombre2 = models.CharField(max_length=100, verbose_name=u'2do Nombre')
    apellido1 = models.CharField(max_length=100, verbose_name=u"1er Apellido")
    apellido2 = models.CharField(max_length=100, verbose_name=u"2do Apellido")
    email = models.CharField(default='', max_length=200, verbose_name=u"Correo electronico")

    class Meta:
        verbose_name = "Persona"
        verbose_name_plural = "Personas"
        ordering = ['id']

    def __str__(self):
        return u'%s %s %s %s' % (self.apellido1, self.apellido2, self.nombre1, self.nombre2)

class ClaseInscrita(ModeloBase):
    persona = models.ForeignKey(Persona, on_delete=models.CASCADE)
    clase = models.ForeignKey(Clase,on_delete=models.CASCADE)
