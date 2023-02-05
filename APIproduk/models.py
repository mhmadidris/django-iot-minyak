# from django.db import models
from djongo import models
# from djongo.models import indexes

class Kategori(models.Model):
    _id = models.ObjectIdField()
    nama = models.CharField(max_length=64)

    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)

    def __str__(self):
        return self.nama
    
class Penukaran(models.Model):
    id_pengguna = models.CharField(max_length=128)
    jumlah = models.IntegerField()
    tanggal = models.DateField(auto_now_add=True)

    class Meta:
        abstract = True
    
class Produk(models.Model):
    _id = models.ObjectIdField()
    nama = models.CharField(max_length=64)
    stok = models.IntegerField()
    keterangan = models.CharField(max_length=128)
    id_mesin = models.CharField(max_length=128)
    gambar = models.CharField(max_length=128)
    poin = models.IntegerField()
    kategori = models.ArrayReferenceField(
        to = Kategori,
        on_delete = models.CASCADE
    )
    penukaran = models.EmbeddedField(
        model_container = Penukaran
    )
    
    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)

    # class Meta: 
    #     indexes = [
    #         indexes.Index. (fields=['nama', 'keterangan'])
    #     ]
    def __str__(self):
        return self.nama
