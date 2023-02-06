from rest_framework import serializers
from APIproduk.models import Produk, Kategori, Penukaran

class ProdukSerializers(serializers.ModelSerializer):
    class Meta: 
        model = Produk
        fields = '__all__'

class KategoriSerializers(serializers.ModelSerializer):

    class Meta: 
        model = Kategori
        fields = '__all__'
        
class PenukaranSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Penukaran
        fields = '__all__'
    
        