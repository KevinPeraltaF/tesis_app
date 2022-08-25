from django.urls import path

from tesis.view_clase import  Ver_Clase
from tesis.view_configuraciones import Configuraciones
from tesis.views import Dashboard, Login, Logout, registrate, PasswordChangeView

urlpatterns = [
    path(r'', Dashboard, name='dashboard'),
    path(r'login/', Login, name='login'),
    path(r'logout/', Logout, name='logout'),
    path(r'registrate/', registrate, name='registrate'),
    path(r'clase/', Ver_Clase, name='clase'),
    path(r'configuracion/', Configuraciones, name='configuraciones'),
    path('change-password/', PasswordChangeView.as_view(), name="CambiarContraseña"),

]
