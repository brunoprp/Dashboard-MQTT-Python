#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 15 19:48:41 2021

@author: bruno
"""
from flask import Flask
from flask import Markup
from flask import Flask
from flask import render_template
import os

app = Flask(__name__)
# Configurando diretorio da pasta das imagens
img_folder = os.path.join('static', 'images')
app.config['UPLOAD_FOLDER'] = img_folder

#%% Controle de cache (Limpa a cahe do navegador)
@app.after_request
def add_header(response):
    response.cache_control.max_age = 0
    return response



@app.route("/")
def chart():
    labels_line =  ["Segunda", "Terça", "Quarta", "Quinta", "Sexta", "Sabado", "Domingo"]
    values_line = [37, 39, 30, 29, 26, 31, 40]
    legend = 'Monthly Data'

    
    labels =['good', 'mediocre','bad']
    values = [30, 10, 12]
    
    full_filename = os.path.join(app.config['UPLOAD_FOLDER'], 'image_mqtt.jpeg')
    
    return render_template('index_2.html', value1= 75 ,value2 = 15 ,
                           labels=labels, 
                           user_image = full_filename, labels_line = labels_line, 
                           values_line = values_line, legend = legend  )




if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)