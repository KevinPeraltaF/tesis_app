from django.urls import path

from tesis.views import dashboard,login

urlpatterns = [
path(r'login', login, name='login'),
    path(r'', dashboard, name='dashboard'),

]
