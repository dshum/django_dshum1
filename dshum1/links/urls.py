from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='links.index'),
    path('create', views.create, name='links.create'),
]
