from django import forms

class ClaseForm(forms.Form):
    nombre = forms.CharField(label='Nombre de la clase ( Obligatorio)', required=False,
                             widget=forms.TextInput(attrs={'class': ' form-control', }))
    seccion = forms.CharField(label='Sección', required=False,
                             widget=forms.TextInput(attrs={'class': 'form-control', }))
    materia = forms.CharField(label='Materia', required=False,
                             widget=forms.TextInput(attrs={'class': 'form-control', }))
    aula = forms.CharField(label='Aula', required=False,
                             widget=forms.TextInput(attrs={'class': 'form-control', }))
