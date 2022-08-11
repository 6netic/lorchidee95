from django.urls import path
from . import views


app_name = 'planning'

urlpatterns = [
    path('index', views.index, name='index'),
    path('display_form', views.display_form, name='display_form'),
    path('check_variables', views.check_variables, name='check_variables'),
    path('extract_lines', views.extract_lines, name='extract_lines'),
    path('check_date_and_is_registered', views.check_date_and_is_registered, name='check_date_and_is_registered'),
    path('insert_tour', views.insert_tour, name='insert_tour'),
    path('display_tour', views.display_tour, name='display_tour'),
    path('save_comment', views.save_comment, name='save_comment'),
    path('validate_line', views.validate_line, name='validate_line'),
]