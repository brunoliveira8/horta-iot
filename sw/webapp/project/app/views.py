# -*- coding: utf-8 -*-
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from .models import Dados
from django.db.models import Avg
import serial


def index(request):
    return render(request, 'index.html')


def umidade(request, valor):
    ser = serial.Serial('/dev/cu.usbserial-AM01P57B')

    ser.write(bytes(valor))

    return HttpResponse('Informação enviada')


def ultima_medida(request):
    dado = Dados.objects.latest('id')
    return JsonResponse({
        'id': dado.id,
        'umidade_solo': dado.umidade_solo,
        'umidade_ar': dado.umidade_ar,
        'temperatura': dado.temperatura,
        'timestamp': dado.criado_em
    })


def media_medidas(request):
    n_medidas = 10
    return JsonResponse(
        Dados.objects.order_by('-criado_em')[:n_medidas].aggregate(Avg('umidade_solo'), Avg('umidade_ar'), Avg('temperatura')),
    )


