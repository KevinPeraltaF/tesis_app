from django.urls import path

from tesis.views import dashboard

urlpatterns = [
    path(r'', dashboard, name='dashboard'),

]
