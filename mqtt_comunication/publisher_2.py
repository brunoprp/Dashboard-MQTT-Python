#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 25 15:23:39 2021

@author: bruno
"""
import paho.mqtt.client as mqtt 
from temperature import measureTemp # Temperatura da CPU
import time

mqttBroker ="192.168.4.62" # Ip do mqttBroker

client = mqtt.Client("Temperature_PC_Bruno") # ID do cliente mqtt

client.connect(mqttBroker)  # Se conectando ao Broker

while True:
    # Publicando a informação no canal TEMPERATURE
    client.publish("TEMPERATURE", "PC_Bruno: "+str(measureTemp())) 
    print("Just published " + "PC_Bruno: "+str(measureTemp()) + " to topic TEMPERATURE")
    # Publicando a cada 1 Segundo
    time.sleep(1)