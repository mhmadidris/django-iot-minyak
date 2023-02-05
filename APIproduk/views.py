from django.shortcuts import render

from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse
from rest_framework import status
from rest_framework.response import Response

from .models import Produk, Kategori
from .serializers import ProdukSerializers, KategoriSerializers
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
                'msg': f'{len(produk.data)} produk ditemukan',
                'data': produk.data
            }, status = status.HTTP_200_OK)
            
        except:
            return JsonResponse({
                'msg': 'Internal server bermasalah',
                'data': []
            }, status = status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET', 'POST'])    
def kategoriMany(req):
    
    try: 
        if req.method == 'GET':
            data = Kategori.objects.all()
            kategori = KategoriSerializers(data, many=True)
            
            return JsonResponse({
                'msg': f'{len(kategori.data)} kategori ditemukan',
                'data': kategori["data"]
            }, status = status.HTTP_200_OK)
            
            
            
        elif req.method == 'POST':
            # data = JSONParser().parse(req)
            # kategoriBaru = KategoriSerializers(data=data, many=True)

            # if kategoriBaru.is_valid():
            #     return JsonResponse({
            #         'msg': 'Kategori baru berhasil ditambahkan',
            #     }, status = status.HTTP_200_OK)
            
            # kategoriBaru.save()
            data = Kategori.objects.all()
            data.create(
                nama = req.data['nama']
            )
                
            return JsonResponse({
                'msg': 'Cek kembali data yang anda masukkan!',
            }, status = status.HTTP_400_BAD_REQUEST)

    except:
        print(sys.exc_info())
        return JsonResponse({
            'msg': 'Internal server bermasalah',
            'data': []
        }, status = status.HTTP_500_INTERNAL_SERVER_ERROR)