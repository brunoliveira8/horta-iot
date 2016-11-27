# -*- coding: utf-8 -*-
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from .models import Dados, Atuador
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

def status_atuador(request):

    st1, st2, st3 = Atuador.objects.order_by('-criado_em')[1:4]

    if st1.status is False:
        duracao_total = st1.criado_em-st2.criado_em
        h, mn, s = str(duracao_total).split(':')
        duracao_min = int(h)*60+int(mn)+float(s)/60

    elif st1.status is True:
        duracao_total = st2.criado_em-st3.criado_em
        h, mn, s = str(duracao_total).split(':')
        duracao_min = int(h)*60+int(mn)+float(s)/60

    return JsonResponse(
       {'duracao': duracao_min, 'status': st1.status, 'timestamp': st1.criado_em},
    )



