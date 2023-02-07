from django.urls import path
from . import views

urlpatterns = [
    path('', views.semuaTransaksi),
    path('add/', views.addTransaksi),
    path('filterday/', views.filterHari),
]
