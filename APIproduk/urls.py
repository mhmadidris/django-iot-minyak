from django.urls import path
from . import views

urlpatterns = [
    path('', views.produkMany),
    path('kategori', views.kategoriMany),
    path('kategori/<str:identifier>', views.kategoriOne)
]
