# -*- coding: utf-8 -*-

import os
import serial
import time

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')

import django
django.setup()

from app.models import Dados


def read_serial():
    ser = serial.Serial('/dev/cu.usbserial-AM01P57B')

    while True:
        # ler

        x = ser.read(10)
        # ser.write(b'hello\n')
        print(x)
        time.sleep(1)


def save_data():
    dados = Dados(umidade_solo=10, umidade_ar=15, temperatura=1)
    dados.save()


def main():
    # read_serial()
    save_data()


if __name__ == '__main__':
    main()
