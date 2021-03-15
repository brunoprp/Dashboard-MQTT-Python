#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 11 14:48:06 2021

@author: bruno
"""
import paho.mqtt.client as mqtt 
import time
from encoder_base64 import ImgEncodDecod64
import os
from random import randrange 

obj_img_base64 = ImgEncodDecod64()

list_imgs = os.listdir("images")


mqttBroker ="sistemas.amsolution.com.br"  #  Ip do mqttBroke port= 1883

client = mqtt.Client("Imagens_Python") # ID do cliente mqtt

client.connect(mqttBroker, port=1883) # Se conectando ao Broker

while True: 
    index_img = randrange(0, 5)
    string_img = obj_img_base64.encoder("images/"+list_imgs[index_img], 'imagem_bin')
    
    client.publish("IMAGEM_BASE64", string_img)
    print("Just published ")
    # Publicando a cada 1 Segundo
    time.sleep(1)
    