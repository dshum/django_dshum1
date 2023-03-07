from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('drama', views.drama, name='experiments.drama'),
]
