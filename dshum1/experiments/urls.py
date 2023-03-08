from django.urls import path

from . import views

urlpatterns = [
    path('drama', views.drama, name='experiments.drama'),
]
