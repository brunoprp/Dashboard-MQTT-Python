#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 18 21:18:18 2021

@author: bruno
"""
import paho.mqtt.client as mqtt
import time
from encoder_base64 import ImgEncodDecod64

obj_img_base64 = ImgEncodDecod64()

data = ''

def on_message(client, userdata, message):
    print("received message: " ,str(message.payload.decode("utf-8")))
    global data 
    data = str(message.payload.decode("utf-8"))

mqttBroker ="sistemas.amsolution.com.br"

client = mqtt.Client("Smartphone")
client.connect(mqttBroker) 



client.loop_start()
client.subscribe("IMAGEM_BASE64")
client.on_message = on_message

# Receder dados do mqttBroker no Canal temperatura por 3 Segundos
time.sleep(15)
client.loop_stop()


# Sanvando a imagem como .bin para decodificar
save_file_bin = "data_imagem"
obj_img_base64.saveStringBin(data, "save_file_bin")

# Decoficando a imagem
name_save_img = "Img_save"
obj_img_base64.decoder("save_file_bin.bin", name_save_img)





