#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 18 20:57:40 2021

@author: bruno
"""
import paho.mqtt.client as mqtt 
from temperature import measureTemp # Temperatura da CPU
import time
from encoder_base64 import ImgEncodDecod64

obj_img_base64 = ImgEncodDecod64()

mqttBroker ="sistemas.amsolution.com.br"  #  Ip do mqttBroke port= 1883

client = mqtt.Client("Temperatura_PC_Edvan_viado") # ID do cliente mqtt
client.connect(mqttBroker, port=1883) # Se conectando ao Broker

string_img = obj_img_base64.encoder('input.jpg', 'imagem_bin')
while True:
    # Publicando a informação no canal TEMPERATURE
    client.publish("TEMPERATURE", "PC_Edvan_viado: "+str(measureTemp()))
    
    client.publish("IMAGEM_BASE64", string_img)
    print("Just published " + "PC_Edvan_viado: "+str(measureTemp()) + " to topic TEMPERATURE")
    # Publicando a cada 1 Segundo
    time.sleep(1)