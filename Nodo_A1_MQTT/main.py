#!/usr/bin/env python
#
#!/usr/bin/env python
#
import binascii
import struct
import _thread
from network import LoRa
from network import WLAN
import socket
import time
import machine
import usocket
import pycom
from mqtt import MQTTClient
from micropython import const


def sub_mqtt(topic, msg):
    if True:
        s = lora()

    if True:
        #distancia = msg.decode()
        distancia = msg.decode()
        s.send(str(distancia))
        #s.send(bytes([0xFF,0xAA, 0xBB, 0xCC, 0xDD, 0xEE, 0xFF]))
        print("Saludo enviado")
        #time.sleep(4)
        #time.sleep(4)
        #time.sleep(4)
        #time.sleep(4)


    print(distancia)

def sub_mqtt_Connect():
    client = MQTTClient("lopy", "192.168.2.1", port=1883)
    client.set_callback(sub_mqtt)
    client.connect()
    client.subscribe(topic="distancia")
    print("Suscrito...")
    while True:
        client.check_msg()


def wlan():
    x = True
    y = True
    wlan = WLAN(mode=WLAN.STA)
    print("Esperando conexion Inalambrica...")
    while x:
        nets = wlan.scan()
        for net in nets:
            if net.ssid == 'broker':
                x = False
                print('Red encontrada - A1')
                wlan.connect(net.ssid, auth=(net.sec, 'broker001'), timeout=5000)
                while not wlan.isconnected():
                    machine.idle() # save power while waiting
                    break
                print('WLAN conexion exitosa!!!')
                break
        time.sleep(5)

def lora():
    lora = LoRa(mode=LoRa.LORAWAN)

    dev_addr = struct.unpack(">l", binascii.unhexlify('26011DA5'.replace(' ','')))[0]#Device Address
    nwk_swkey = binascii.unhexlify('9E8262DC2B9787CA600C5CF46F25CC55'.replace(' ',''))# Network Session Key
    app_swkey = binascii.unhexlify('77F84AF9B49326ACE2E1F0CB18A79FB0'.replace(' ',''))# App Session Key

    for channel in range(3, 16):
        lora.remove_channel(channel)

    # set the  channels  frequency
    lora.add_channel(0, frequency=868100000, dr_min=0, dr_max=5)
    lora.add_channel(1, frequency=868100000, dr_min=0, dr_max=5)
    lora.add_channel(2, frequency=868100000, dr_min=0, dr_max=5)

    # join a network using ABP (Activation By Personalization)
    lora.join(activation=LoRa.ABP, auth=(dev_addr, nwk_swkey, app_swkey))

    for i in range(3, 16):
        lora.remove_channel(i)


    s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)
    s.setsockopt(socket.SOL_LORA, socket.SO_DR, 5)
    s.setblocking(False)

    return s

wlan()
sub_mqtt_Connect()
