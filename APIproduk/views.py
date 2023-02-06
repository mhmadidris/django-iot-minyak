from django.shortcuts import render

from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse
from rest_framework import status
from rest_framework.response import Response

from .models import Produk, Kategori
from .serializers import ProdukSerializers, KategoriSerializers, PenukaranSerializer
from bson.objectid import ObjectId 
from rest_framework.decorators import api_view

from django.core.exceptions import ObjectDoesNotExist
from bson.errors import InvalidId

import sys
import json
from operator import itemgetter

# API UNTUK BANYAK PRODUK 
@api_view(['GET', 'POST'])
def produkMany(req):
    
    try: 
        if req.method == 'GET':
            q = req.GET.get('q', None)
            k = req.GET.get('k', None)
            sortBy = req.GET.get('sortby', None)
            
            if q is not None or k is not None:
                
                # filter berdasarkan kata kunci
                if sortBy is not None:
                    data = Produk.objects.filter(nama__icontains=q).filter(kategori__icontains=k).order_by(sortBy)
                else:    
                    data = Produk.objects.filter(nama__icontains=q).filter(kategori__icontains=k)

            else:
                if sortBy is not None:
                    data = Produk.objects.all().order_by(sortBy)
                else:
                    data = Produk.objects.all()
                
            produk = ProdukSerializers(data, many=True)

            for item in produk.data:
                item['penukaran'] = json.loads(item['penukaran'].replace('\'','\"'))

            # tampilkan data dan jumlahnya 
            return JsonResponse({
                'pesan': f'{len(produk.data)} produk ditemukan',
                'data': produk.data
            }, status = status.HTTP_200_OK)
            
        elif req.method == 'POST':
            data = JSONParser().parse(req)
            
            data["kategori"] = ','.join(data["kategori"])

            produkBaru = ProdukSerializers(data=data)

            # cek validasi lalu simpan 
            if produkBaru.is_valid():
                produkBaru.save()

                return JsonResponse({
                    'pesan': 'Produk baru berhasil ditambahkan',
                }, status = status.HTTP_200_OK)
            
            # data yg dikirimkan invalid 
            print(produkBaru.errors)
                
            return JsonResponse({
                'pesan': 'Cek kembali data yang anda masukkan!',
            }, status = status.HTTP_400_BAD_REQUEST)
            
        
    except:
        print(sys.exc_info())
        
        return JsonResponse({
            'pesan': 'Internal server bermasalah',
            'data': []
        }, status = status.HTTP_500_INTERNAL_SERVER_ERROR)

# API UNTUK SATU KATEGORI 
@api_view(['GET', 'PUT', 'DELETE'])    
def produkOne(req, identifier):
    
    try:
        # ambil dulu satu kategori 
        data = Produk.objects.get(pk=ObjectId(identifier))

        # dapatkan kategori 
        if req.method == 'GET':
            produk = ProdukSerializers(data)

            produkData = produk.data
            produkData['penukaran'] = json.loads(produk.data['penukaran'].replace('\'','\"'))

            return JsonResponse({
                'pesan': f'Produk ditemukan',
                'data': produkData,
                # 'tes':json.loads(produk.data['penukaran'].replace('\'','\"'))
            }, status = status.HTTP_200_OK)
        
        # edit kategori 
        elif req.method == 'PUT':
            dataBaru = JSONParser().parse(req)
            
            if 'kategori' in dataBaru:
                dataBaru["kategori"] = ','.join(dataBaru["kategori"])
            
            produkBaru = KategoriSerializers(data, data=dataBaru)

            # cek validasi data 
            if produkBaru.is_valid():
                produkBaru.save()

                return JsonResponse({
                    'pesan': 'Produk berhasil diperbaharui',
                }, status = status.HTTP_200_OK)
            
            # data yg dikirimkan invalid 
            print(produkBaru.errors)
                
            return JsonResponse({
                'pesan': 'Cek kembali data yang anda masukkan!',
            }, status = status.HTTP_400_BAD_REQUEST)
                
        # hapus kategori 
        elif req.method == 'DELETE':
            data.delete()

            return JsonResponse({
                'pesan': 'Produk berhasil di hapus!'
            })
          
    except InvalidId:
        return JsonResponse({
            'pesan': 'Produk tidak ditemukan!',
            'data': []
        }, status = status.HTTP_404_NOT_FOUND)     

    except:
        # jika sistem error 
        print(sys.exc_info())
        return JsonResponse({
            'pesan': 'Internal server bermasalah',
            'data': []
        }, status = status.HTTP_500_INTERNAL_SERVER_ERROR)
 

# ------------------------- 

# API UNTUK BANYAK KATEGORI 
@api_view(['GET', 'POST'])    
def kategoriMany(req):
    
    try:  
        # cari semua
        if req.method == 'GET':
            q = req.GET.get('q', None)
            sortBy = req.GET.get('sortby', None)
            
            if q is not None:
                
                # filter berdasarkan kata kunci
                if sortBy is not None:
                    data = Kategori.objects.filter(nama__icontains=q).order_by(sortBy)
                else:    
                    data = Kategori.objects.filter(nama__icontains=q)

            else:
                if sortBy is not None:
                    data = Kategori.objects.all().order_by(sortBy)
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

        print(ObjectId(identifier))
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
    
    except InvalidId:
        return JsonResponse({
            'pesan': 'Kategori tidak ditemukan!',
            'data': []
        }, status = status.HTTP_404_NOT_FOUND)     

    except:
        # jika sistem error 
        print(sys.exc_info())
        return JsonResponse({
            'pesan': 'Internal server bermasalah',
            'data': []
        }, status = status.HTTP_500_INTERNAL_SERVER_ERROR)
        