from django.urls import path, include
from .views import cozinhar, lista_estoque

urlpatterns = [
    path('cozinhar/', cozinhar, name='cozinhar'),
    path('estoque/', lista_estoque, name='estoque')
]