import sys

from django.shortcuts import render

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