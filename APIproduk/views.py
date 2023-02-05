from django.shortcuts import render

from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse
from rest_framework import status
from rest_framework.response import Response

from .models import Produk, Kategori
from .serializers import ProdukSerializers, KategoriSerializers
from bson.objectid import ObjectId 
from rest_framework.decorators import api_view

import sys

@api_view(['GET', 'POST'])
def produkMany(req):
    
    if req.method == 'GET':
        
        try: 
            q = req.GET.get('q', None)

            # search kata kunci nama dan keterangan 
            if q is not None:
                data = Produk.objects.filter(nama__icontains=q)
            else:
                data = Produk.objects.all()

            produk = ProdukSerializers(data, many=True)

            return JsonResponse({
                'pesan': f'{len(produk.data)} produk ditemukan',
                'data': produk.data
            }, status = status.HTTP_200_OK)
            
        except:
            return JsonResponse({
                'pesan': 'Internal server bermasalah',
                'data': []
            }, status = status.HTTP_500_INTERNAL_SERVER_ERROR)

# API UNTUK BANYAK KATEGORI 
@api_view(['GET', 'POST'])    
def kategoriMany(req):
    
    try: 
        
        # cari semua
        if req.method == 'GET':
            q = req.GET.get('q', None)

            if q is not None:
                # filter berdasarkan kata kunci
                data = Kategori.objects.filter(nama__icontains=q)
            else:
                data = Kategori.objects.all()
                
            kategori = KategoriSerializers(data, many=True)
            
            # tampilkan data dan jumlahnya 
            return JsonResponse({
                'pesan': f'{len(kategori.data)} kategori ditemukan',
                'data': kategori.data
            }, status = status.HTTP_200_OK)
            
        # bikin satu kategori 
        elif req.method == 'POST':
            data = JSONParser().parse(req)
            kategoriBaru = KategoriSerializers(data=data)

            # cek validasi lalu simpan 
            if kategoriBaru.is_valid():
                kategoriBaru.save()

                return JsonResponse({
                    'pesan': 'Kategori baru berhasil ditambahkan',
                }, status = status.HTTP_200_OK)
            
            # data yg dikirimkan invalid 
            print(kategoriBaru.errors)
                
            return JsonResponse({
                'pesan': 'Cek kembali data yang anda masukkan!',
            }, status = status.HTTP_400_BAD_REQUEST)

    except:
        # jika sistem error kasih response status 500 
        print(sys.exc_info())
        return JsonResponse({
            'pesan': 'Internal server bermasalah',
            'data': []
        }, status = status.HTTP_500_INTERNAL_SERVER_ERROR)
    
# API UNTUK SATU KATEGORI 
@api_view(['GET', 'PUT', 'DELETE'])    
def kategoriOne(req, identifier):
    
    try:
        # ambil dulu satu kategori 
        data = Kategori.objects.get(pk=ObjectId(identifier))

        # dapatkan kategori 
        if req.method == 'GET':
            kategori = KategoriSerializers(data)
            
            return JsonResponse({
                'pesan': f'kategori ditemukan',
                'data': kategori.data
            }, status = status.HTTP_200_OK)
        
        # edit kategori 
        elif req.method == 'PUT':
            dataBaru = JSONParser().parse(req)
            kategoriBaru = KategoriSerializers(data, data=dataBaru)

            # cek validasi data 
            if kategoriBaru.is_valid():
                kategoriBaru.save()

                return JsonResponse({
                    'pesan': 'Kategori berhasil diperbaharui',
                }, status = status.HTTP_200_OK)
            
            # data yg dikirimkan invalid 
            print(kategoriBaru.errors)
                
            return JsonResponse({
                'pesan': 'Cek kembali data yang anda masukkan!',
            }, status = status.HTTP_400_BAD_REQUEST)
                
        # hapus kategori 
        elif req.method == 'DELETE':
            data.delete()

            return JsonResponse({
                'pesan': 'Kategori berhasil di hapus!'
            })
                
    except:
        # jika sistem error 
        print(sys.exc_info())
        return JsonResponse({
            'pesan': 'Internal server bermasalah',
            'data': []
        }, status = status.HTTP_500_INTERNAL_SERVER_ERROR)
        