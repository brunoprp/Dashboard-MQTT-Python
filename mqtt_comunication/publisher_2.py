#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 25 15:23:39 2021

@author: bruno
"""
import paho.mqtt.client as mqtt 
from pyspectator.processor import Cpu
from random import randrange, uniform
import time

mqttBroker ="192.168.4.62" 

client = mqtt.Client("Temperature_PC_Bruno")
client.connect(mqttBroker) 

while True:
    cpu = Cpu(monitoring_latency=1)
    client.publish("TEMPERATURE", "PC_Bruno: "+str(cpu.temperature))
    
    print("Just published " + "PC_Bruno: "+str(cpu.temperature) + " to topic TEMPERATURE")
    time.sleep(1)