from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.forms import DateTimeInput

from tesis.models import MetodoCalificacion, DetalleMetodoCalificacion


class ClaseForm(forms.Form):
    nombre = forms.CharField(label='Nombre del curso ( Obligatorio)', required=False,
                             widget=forms.TextInput(attrs={'class': ' form-control', }))
    seccion = forms.CharField(label='Sección', required=False,
                             widget=forms.TextInput(attrs={'class': 'form-control', }))
    materia = forms.CharField(label='Materia', required=False,
                             widget=forms.TextInput(attrs={'class': 'form-control', }))
    aula = forms.CharField(label='Aula', required=False,
                             widget=forms.TextInput(attrs={'class': 'form-control', }))

    metodocalificacion= forms.ModelChoiceField(required=True, queryset=MetodoCalificacion.objects.filter(status=True).order_by('id'),
                             label=u'Mètodo de Calificación',  widget=forms.Select(attrs={'class': 'form-control'}))



class PersonaForm(forms.Form):
    nombre1 = forms.CharField(label='1ª Nombre', required=True,
                             widget=forms.TextInput(attrs={'class': ' form-control', }))
    nombre2 = forms.CharField(label='2ª Nombre', required=True,
                             widget=forms.TextInput(attrs={'class': 'form-control', }))
    apellido1 = forms.CharField(label='1ª Apellido', required=True,
                             widget=forms.TextInput(attrs={'class': 'form-control', }))
    apellido2 = forms.CharField(label='2º Apellido', required=True,
                             widget=forms.TextInput(attrs={'class': 'form-control', }))
    email = forms.CharField(label=u"Correo electrónico", max_length=200, required=True,
                            widget=forms.TextInput(attrs={'class': 'form-control',}))




class RegistroUsuarioForm(UserCreationForm):

    def __init__(self, *args, **kwargs):
        super(RegistroUsuarioForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            self.fields['password1'].widget.attrs['class'] = "form-control"
            self.fields['password2'].widget.attrs['class'] = "form-control"

    email = forms.EmailField(label="Email", widget=forms.TextInput(attrs={'class': 'form-control', }))
    nombre1 = forms.CharField(label="1er. Nombre", widget=forms.TextInput(attrs={'class': 'form-control', }))
    nombre2 = forms.CharField(label="2do. Nombre", widget=forms.TextInput(attrs={'class': 'form-control', }))
    apellido1 = forms.CharField(label="Apellido paterno", widget=forms.TextInput(attrs={'class': 'form-control', }))
    apellido2 = forms.CharField(label="Apellido materno", widget=forms.TextInput(attrs={'class': 'form-control', }))



    def clean_username(self):
        username = self.cleaned_data['username'].lower()
        r = User.objects.filter(username=username)
        if r.count():
            raise ValidationError("Nombre de usuario ya existe.")
        return username

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        r = User.objects.filter(email=email)
        if r.count():
            raise ValidationError("Email ya existe")
        return email

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise ValidationError("La contraseña no coincide.")

        return password2

    class Meta:
        model = User
        fields = ("username", "email",)

        widgets = {
            'username': forms.TextInput(
                attrs={
                    'class': 'form-control',

                }
            ),
        }


class UnirmeClaseForm(forms.Form):
    codigo_clase = forms.CharField(label='Código del curso', required=True, max_length=7,
                             widget=forms.TextInput(attrs={'class': ' form-control', }))


class FormularioGeneralPublicacion(forms.Form):
    titulo = forms.CharField(label='Titulo', required=False,
                             widget=forms.TextInput(attrs={'class': ' form-control', }))
    instrucciones = forms.CharField(label=u'Instrucciones', required=False,
                                    widget=forms.Textarea(attrs={'class': ' form-control', 'rows': '5'}))


class CrearTareaForm(FormularioGeneralPublicacion):
    fecha_fin_entrega = forms.DateField(label="Fecha Fin de entrega",input_formats=['%d-%m-%Y'],
                            widget=DateTimeInput(format='%d-%m-%Y',attrs={'class': 'form-control'}), required=False)


class CrearMaterialForm(FormularioGeneralPublicacion):
    archivo= forms.FileField(label='Archivo', required=True, widget=forms.ClearableFileInput(attrs={'class': 'dropify', 'data-allowed-file-extensions': 'pdf docx' }))



class CrearVideoForm(FormularioGeneralPublicacion):
    urlvideo= forms.CharField(label='Url video', required=True, widget=forms.TextInput(attrs={'class': ' form-control', }))



class SubirTareaForm(forms.Form):
    archivo= forms.FileField(label='Subir Tarea', required=True, widget=forms.ClearableFileInput(attrs={'class': 'dropify', 'data-allowed-file-extensions': 'pdf docx' }))



class MetodoCalifcacionForm(forms.Form):
    nombre = forms.CharField(label='Método de calificación', required=False,
                             widget=forms.TextInput(attrs={'class': ' form-control', }))

    nota_aprobacion = forms.IntegerField(label='Calificación máxima', required=False,
                                             widget=forms.TextInput(attrs={'class': ' form-control', }))



class DetalleMetodoCalificacionForm(forms.Form):

    nombre = forms.CharField(label='Modelo de calificación', required=False,
                             widget=forms.TextInput(attrs={'class': ' form-control', }))
    nota_aprobacion = forms.IntegerField(label='Calificación máxima', required=False,
                                         widget=forms.TextInput(attrs={'class': ' form-control', }))

class CampoDetalleMetodoCalificacionForm(forms.Form):

    nombre = forms.CharField(label='Campo', required=False,
                             widget=forms.TextInput(attrs={'class': ' form-control', }))
    nota_aprobacion = forms.IntegerField(label='Calificación máxima', required=False,
                                         widget=forms.TextInput(attrs={'class': ' form-control', }))
