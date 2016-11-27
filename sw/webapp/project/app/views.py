# -*- coding: utf-8 -*-
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from .models import Dados, Atuador, Configuracao
from django.db.models import Avg
from django.views.generic import View
from .forms import ConfiguracaoForm
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
import serial


@login_required(login_url='/accounts/login/')
def index(request):
    return render(request, 'index.html')


def umidade(request, valor):
    ser = serial.Serial('/dev/cu.usbserial-AM01P57B')

    ser.write(bytes(valor))

    return HttpResponse('Informação enviada')


@login_required(login_url='/accounts/login/')
def ultima_medida(request):
    dado = Dados.objects.latest('id')
    return JsonResponse({
        'id': dado.id,
        'umidade_solo': dado.umidade_solo,
        'umidade_ar': dado.umidade_ar,
        'temperatura': dado.temperatura,
        'timestamp': dado.criado_em
    })


@login_required(login_url='/accounts/login/')
def media_medidas(request):
    n_medidas = 10
    return JsonResponse(
        Dados.objects.order_by('-criado_em')[:n_medidas].aggregate(
            Avg('umidade_solo'), Avg('umidade_ar'), Avg('temperatura')),
    )


@login_required(login_url='/accounts/login/')
def status_atuador(request):

    st1, st2, st3 = Atuador.objects.order_by('-criado_em')[:3]

    if st1.status is False:
        duracao_total = st1.criado_em - st2.criado_em
        h, mn, s = str(duracao_total).split(':')
        duracao_min = int(h) * 60 + int(mn) + float(s) / 60

    elif st1.status is True:
        duracao_total = st2.criado_em - st3.criado_em
        h, mn, s = str(duracao_total).split(':')
        duracao_min = int(h) * 60 + int(mn) + float(s) / 60

    return JsonResponse(
        {'duracao': duracao_min, 'status': st1.status, 'timestamp': st1.criado_em},
    )


class ConfiguracaoView(View):

    def get(self, request):
        context_dict = dict()
        try:
            old_config = Configuracao.objects.get(pk=0)
            form = ConfiguracaoForm(instance=old_config)
        except:
            form = ConfiguracaoForm()

        context_dict['form'] = form
        return render(request, 'configurar.html', context_dict)

    def post(self, request):
        context_dict = dict()
        form = ConfiguracaoForm(request.POST)

        context_dict['form'] = form

        if form.is_valid():
            # Save the new category to the database.
            new_config = form.save(commit=False)
            config = Configuracao.objects.update_or_create(
                pk=0,
                defaults={
                    'teto': new_config.teto,
                    'piso': new_config.piso,
                    'intervalo': new_config.intervalo
                }
            )

            # ser = serial.Serial('/dev/cu.usbserial-AM01P57B')
            # dados = "{0};{1};{2}".format(new_config.teto, new_config.piso, intervalo)
            # ser.write(bytes(dados))

            return render(request, 'success.html', context_dict)

        return render(request, 'configurar.html', context_dict)

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ConfiguracaoView, self).dispatch(*args, **kwargs)
