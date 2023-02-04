from django.shortcuts import redirect
from rest_framework.decorators import api_view
from .models import Minyak, Poin
from .serializers import MinyakSerializers, PoinSerializer
from rest_framework.response import Response


@api_view(["GET"])
def listMinyak(request):
    data = Minyak.objects.all()
    serializer = MinyakSerializers(data, many=True)
    return Response(serializer.data)


#Input minyak + update poin
@api_view(["POST"])
def addMinyak(request):
    minyak = Minyak.objects.create(
        user = request.data["user"],
        volume = request.data["volume"]
    )
    try:
        Poin.objects.create(
            user = request.data["user"],
            # Rumus poin
            poin = (int(minyak.volume) * 100)
        )
    except:
        poin = int(Poin.objects.get(user = request.data["user"]).poin + (minyak.volume * 100))
        updatePoin = Poin.objects.filter(user = request.data["user"])
        updatePoin.update(
            poin = poin
        )
    return redirect('/api/')


@api_view(["GET"])
def PoinView(request):
    data = Poin.objects.all()
    serializer = PoinSerializer(data, many=True)
    return Response(serializer.data)

# @api_view(["GET"])
# def detailMinyak(request,username):
#     data = Minyak.objects.filter(user = username)
#     serializer = MinyakSerializers(data, many=True)
#     return Response(serializer.data)

# @api_view(["DELETE"])
# def deleteMinyak(request, delete_id):
#     minyak = Minyak.objects.get(id = delete_id)
#     poin = Poin.objects.get(user = minyak.user).poin
#     poin = poin - (int(minyak.volume) * 100)
#     Poin.objects.filter(user = minyak.user).update(
#         poin = poin
#     )
#     minyak = Minyak.objects.filter(id = delete_id).delete()
#     return redirect('/api/')