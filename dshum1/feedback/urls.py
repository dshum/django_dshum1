from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='feedback.index'),
    path('create', views.create, name='feedback.create'),
]
