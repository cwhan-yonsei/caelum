from django.urls import path, include
from . import views

app_name = 'air'

urlpatterns = [
    path('', views.index, name='index'),
]