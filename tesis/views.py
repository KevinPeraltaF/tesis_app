import sys

from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import render

# Create your views here.
def dashboard(request):
    global ex
    data = {}
    if request.method == 'POST':
        if 'peticion' in request.POST:
            peticion = request.POST['peticion']
    else:
        if 'peticion' in request.GET:
            peticion = request.GET['peticion']

        else:
            try:
                data['titulo'] = 'Menú principal'

                return render(request, "registration/dashboard.html ", data)
            except Exception as ex:
                print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno))

def login(request):
    global ex
    data = {}
    if request.method == 'POST':
        if 'peticion' in request.POST:
            peticion = request.POST['peticion']
    else:
        if 'peticion' in request.GET:
            peticion = request.GET['peticion']

        else:
            try:
                data['titulo'] = 'Inicio de Sesion'

                return render(request, "registration/login.html ", data)
            except Exception as ex:
                print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno))

