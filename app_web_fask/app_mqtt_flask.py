#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 13 14:58:22 2021

@author: bruno
"""

from flask import Flask, render_template
from flask_mqtt import Mqtt
from flask_socketio import SocketIO
import time
import os
from encoder_base64 import ImgEncodDecod64

#%% Instancias
obj_base64 = ImgEncodDecod64() # Instanciando o objeto da classe ImgEncodDecod64()

# Criando o app flask e configurando a comunicação MQTT
app = Flask(__name__)
app.config['MQTT_BROKER_URL'] = 'sistemas.amsolution.com.br'
app.config['MQTT_BROKER_PORT'] = 1883
app.config['MQTT_REFRESH_TIME'] = 1.0

# Configurando diretorio da pasta das imagens
img_folder = os.path.join('static', 'images')
app.config['UPLOAD_FOLDER'] = img_folder

img_string = '' # Mensagem recebida pelo MQTT
file_name_img = "image_mqtt" # Nome do arquivo da imagem
path_img = "static/images/" # Onde a imagem vai ser salva
mqtt = Mqtt(app) # Instaciando o objeto MQTT com o app Flask
socketio = SocketIO(app) # Integrando o objeto socketi a aplicação


#%% Rota Proincipal da aplicação que renderiza o site
@app.route('/')
def index():
    # Caminho da imagem salva
    full_filename = os.path.join(app.config['UPLOAD_FOLDER'], 'image_mqtt.jpeg')
    return  render_template("index.html", user_image = full_filename)


#%% Controle de cache (Limpa a cahe do navegador)
@app.after_request
def add_header(response):
    response.cache_control.max_age = 0
    return response

#%% Subscriber no topico IMAGEM_BASE64
@mqtt.on_connect()
def handle_connect(client, userdata, flags, rc):
    mqtt.subscribe('IMAGEM_BASE64')


#%% Recebendo a mensagem do topico do MQTT
@mqtt.on_message()
def handle_mqtt_message(client, userdata, message):
    global img_string 
    data = dict(
        topic=message.topic,
        payload=message.payload.decode()
    )
    # Salvando a mensagem e fazendo o deconder da imagem 
    img_string = message.payload.decode()
    obj_base64.saveStringBin(img_string, "arquivos/imagem_bin")
    time.sleep(5)
    obj_base64.decoder("arquivos/imagem_bin.bin", path_img+file_name_img)
    
   
#%% Mostrando informações das mensagen recebidas
@mqtt.on_log()
def handle_logging(client, userdata, level, buf):
    print(level, buf)

#%% Execultado toda a aplicação
if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, use_reloader=True, debug=True)
    
    
    
    
    
    