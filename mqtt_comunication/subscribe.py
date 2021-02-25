#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 18 21:18:18 2021

@author: bruno
"""
import paho.mqtt.client as mqtt
import time

def on_message(client, userdata, message):
    print("received message: " ,str(message.payload.decode("utf-8")))

mqttBroker ="192.168.4.62"

client = mqtt.Client("Smartphone")
client.connect(mqttBroker) 




client.loop_start()
client.subscribe("TEMPERATURE")
client.on_message=on_message
    
   
# Receder dados do mqttBroker no Canal temperatura por 10 Segundos
time.sleep(10)
client.loop_stop()

