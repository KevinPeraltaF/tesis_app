import sys

from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import render
@login_required(redirect_field_name='next', login_url='/login')
@transaction.atomic()
def Clase(request):
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

                return render(request, "clase/clase.html ", data)
            except Exception as ex:
                print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno))