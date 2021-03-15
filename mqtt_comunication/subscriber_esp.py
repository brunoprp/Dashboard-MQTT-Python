#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 10 12:07:30 2021

@author: bruno
"""

import paho.mqtt.client as mqtt
import time
from encoder_base64 import ImgEncodDecod64

obj_img_base64 = ImgEncodDecod64()

data = []

def imgEspDecod(list_string):
    img_string = ''
    for string in list_string:
        if string == 'INICIO' or string == "FIM":
            pass
        else:
           img_string += string
    return img_string
    

def on_message(client, userdata, message):
    
    #print("received message: " ,str(message.payload.decode("utf-8")))
    global data
    data.append(str(message.payload.decode("utf-8")))

    if str(message.payload.decode("utf-8")) == "FIM":
        print("Saiu")
        client.loop_stop()



mqttBroker ="sistemas.amsolution.com.br"

client = mqtt.Client("Smartphone")
client.connect(mqttBroker) 



client.loop_start()
client.subscribe("ESP32_envia_informacao")
client.on_message = on_message



string_img = imgEspDecod(data)


obj_img_base64.saveStringBin(string_img, "img_bin_esp")

obj_img_base64.decoder("img_bin_esp.bin", "image_esp")

#time.sleep(15)
# Receder dados do mqttBroker no Canal temperatura por 3 Segundos
#
#if "FIM" in data:
    #print("Saiu")
    #client.loop_stop()

"""
# Sanvando a imagem como .bin para decodificar
save_file_bin = "data_imagem"
obj_img_base64.saveStringBin(data, "save_file_bin")

# Decoficando a imagem
name_save_img = "Img_save"
obj_img_base64.decoder("save_file_bin.bin", name_save_img)
"""

