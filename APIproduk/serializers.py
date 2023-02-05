from rest_framework import serializers
from APIproduk.models import Produk, Kategori

class ProdukSerializers(serializers.ModelSerializer):
    class Meta: 
        model = Produk
        fields = ('__all__')

class KategoriSerializers(serializers.ModelSerializer):
    class Meta: 
        model = Kategori
        fields = '__all__'
        