#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 13 14:58:22 2021

@author: bruno
"""

from flask import Flask, render_template
from flask_mqtt import Mqtt
from flask_socketio import SocketIO
from flask_caching import Cache
import time
import os


from encoder_base64 import ImgEncodDecod64

obj_base64 = ImgEncodDecod64()
cache = Cache()
app = Flask(__name__)
cache.init_app(app)


app.config['MQTT_BROKER_URL'] = 'sistemas.amsolution.com.br'
app.config['MQTT_BROKER_PORT'] = 1883
app.config['MQTT_REFRESH_TIME'] = 1.0


img_folder = os.path.join('static', 'images')
app.config['UPLOAD_FOLDER'] = img_folder

img_string = ''
file_name_img = "image_mqtt"
path_img = "static/images/"
mqtt = Mqtt(app)
socketio = SocketIO(app)


@app.route('/')
@cache.cached(timeout = 1)
def index():
    full_filename = os.path.join(app.config['UPLOAD_FOLDER'], 'image_mqtt.jpeg')
    
    return  render_template("index.html", user_image = full_filename)




@mqtt.on_connect()
def handle_connect(client, userdata, flags, rc):
    mqtt.subscribe('IMAGEM_BASE64')

@mqtt.on_message()
def handle_mqtt_message(client, userdata, message):
    global img_string 
    data = dict(
        topic=message.topic,
        payload=message.payload.decode()
    )
    img_string = message.payload.decode()
    
    obj_base64.saveStringBin(img_string, "imagem_bin")
    
    time.sleep(5)
    
    obj_base64.decoder("imagem_bin.bin", path_img+file_name_img)
    
    
    # emit a mqtt_message event to the socket containing the message data
    #socketio.emit('mqtt_message', data=data)
    
    

@mqtt.on_log()
def handle_logging(client, userdata, level, buf):
    print(level, buf)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, use_reloader=True, debug=True)
    
    
    
    
    
    