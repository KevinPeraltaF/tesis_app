from django.urls import path

from tesis.view_clase import Clase
from tesis.views import Dashboard, Login

urlpatterns = [
    path(r'login', Login, name='login'),
    path(r'clase', Clase, name='clase'),
    path(r'', Dashboard, name='dashboard'),

]
