# -*- coding: utf-8 -*-

# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render
import serial

def index(request):
     return render(request, 'index.html')

def umidade(request, valor):
    ser = serial.Serial('/dev/cu.usbserial-AM01P57B')

    ser.write(bytes(valor))

    return HttpResponse('Informação enviada')
