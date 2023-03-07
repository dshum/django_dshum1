from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='shortener.index'),
    path('create', views.create, name='shortener.create'),
    path('<str:short_url>', views.redirect_url, name='shortener.redirect'),
]
