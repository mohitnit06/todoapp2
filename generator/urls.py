from . import views
from django.urls import path

app_name = 'generator'

urlpatterns = [
    path('', views.input, name='input'),
    path('password', views.password_generated),
]
