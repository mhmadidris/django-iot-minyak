from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('mesin/', include('APImesin.urls')),
    path('produk/', include('APIproduk.urls')),
    path('users/', include('APIUserManagement.urls')),
    path('', include('APIAuth.urls')),
]
