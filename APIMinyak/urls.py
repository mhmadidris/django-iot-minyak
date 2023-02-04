from django.urls import path
from . import views

urlpatterns = [
    path('',views.listMinyak),
    path('add/',views.addMinyak),
    path('poin/',views.PoinView),
]
