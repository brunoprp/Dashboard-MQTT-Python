#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 18 20:57:40 2021

@author: bruno
"""
import paho.mqtt.client as mqtt 
from pyspectator.processor import Cpu
import time

mqttBroker ="192.168.4.62" 

client = mqtt.Client("Temperatura_PC_Edvan_viado")
client.connect(mqttBroker) 

while True:
    cpu = Cpu(monitoring_latency=1)
    client.publish("TEMPERATURE", "PC_Edvan_viado: "+str(cpu.temperature))
    print("Just published " + "PC_Edvan_viado: "+str(cpu.temperature) + " to topic TEMPERATURE")
    time.sleep(1)