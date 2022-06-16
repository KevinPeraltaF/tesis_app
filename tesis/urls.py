from django.urls import path

from tesis.view_clase import Clase
from tesis.views import Dashboard, Login, Logout

urlpatterns = [
    path(r'', Dashboard, name='dashboard'),
    path(r'login/', Login, name='login'),
    path(r'logout/', Logout, name='logout'),
    path(r'clase/', Clase, name='clase'),


]
