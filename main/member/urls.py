from django.urls import path
from . import views


app_name = 'member'

urlpatterns = [
    path('connect', views.connect, name='connect'),
    path('disconnect', views.disconnect, name='disconnect'),
    path('modify_password', views.modify_password, name='modify_password'),
]