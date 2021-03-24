#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 22 15:06:05 2021

@author: bruno
"""
from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
from flask_socketio import SocketIO
from flask_mqtt import Mqtt
from encoder_base64 import ImgEncodDecod64
import time
import re
import os

app = Flask(__name__)

# Enter your database connection details below
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'bruno'
app.config['MYSQL_PASSWORD'] = 'Cavalo_321'
app.config['MYSQL_DB'] = 'IOT'

# Intialize MySQL
mysql = MySQL(app)

app.secret_key = 'IOT'


#%% Instancias
obj_base64 = ImgEncodDecod64() # Instanciando o objeto da classe ImgEncodDecod64()

#  Configurando a comunicação MQT
app.config['MQTT_BROKER_URL'] = 'sistemas.amsolution.com.br'
app.config['MQTT_BROKER_PORT'] = 1883
app.config['MQTT_REFRESH_TIME'] = 1.0

img_string = '' # Mensagem recebida pelo MQTT (Imagem em base64)
valor_temp1 = '50'

file_name_img = "image_mqtt" # Nome do arquivo da imagem
path_img = "static/images/" # Onde a imagem vai ser salva
mqtt = Mqtt(app) # Instaciando o objeto MQTT com o app Flask
socketio = SocketIO(app) # Integrando o objeto socketi a aplicação


# Configurando diretorio da pasta das imagens
img_folder = os.path.join('static', 'images')
app.config['UPLOAD_FOLDER'] = img_folder

folder_temp = "arquivos/temperatura.txt"


#%% Controle de cache (Limpa a cahe do navegador)
@app.after_request
def add_header(response):
    response.cache_control.max_age = 0
    return response




#%% Pagina de longin

@app.route('/', methods=['GET', 'POST'])
def login():
    # Output message if something goes wrong...
    msg = ''
    # Check if "username" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        
        
        # Check if account exists using MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM usuarios WHERE username = %s AND password = %s',
                       (username, password,))
        # Fetch one record and return result
        account = cursor.fetchone()
        
        
        # If account exists in accounts table in out database
        if account:
            # Create session data, we can access this data in other routes
            session['loggedin'] = True
            session['id'] = account['id']
            session['username'] = account['username']
            # Redirect to home page
            return redirect(url_for('home'))
        else:
            # Account doesnt exist or username/password incorrect
            msg = 'Incorrect username/password!'
    # Show the login form with message (if any)
    
    return render_template('login.html', msg=msg)

#%% Faz o ação do logout para deslogar o usuario

@app.route('/logout')
def logout():
    # Remove session data, this will log the user out
   session.pop('loggedin', None)
   session.pop('id', None)
   session.pop('username', None)
   # Redirect to login page
   return redirect(url_for('login'))


#%% Registro de usuario no banco de dados
@app.route('/register', methods=['GET', 'POST'])
def register():
    # Output message if something goes wrong...
    msg = ''
    # Check if "username", "password" and "email" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        
        # Check if account exists using MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM usuarios WHERE username = %s', (username,))
        account = cursor.fetchone()
        # If account exists show error and validation checks
        if account:
            msg = 'Account already exists!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address!'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers!'
        elif not username or not password or not email:
            msg = 'Please fill out the form!'
        else:
            # Account doesnt exists and the form data is valid, now insert new account into accounts table
            cursor.execute('INSERT INTO usuarios VALUES (NULL, %s, %s, %s)', (username, password, email,))
            mysql.connection.commit()
            msg = 'You have successfully registered!'
        
    elif request.method == 'POST':
        # Form is empty... (no POST data)
        msg = 'Please fill out the form!'
    # Show registration form with message (if any)
    return render_template('register.html', msg=msg)



    
#%% Graficos individuais 






#%% Dados MQTT 

# Subscriber no topico IMAGEM_BASE64
@mqtt.on_connect()
def handle_connect(client, userdata, flags, rc):
    mqtt.subscribe('IMAGEM_BASE64')
    mqtt.subscribe('temperatura')


# Recebendo a mensagem do topico do MQTT
@mqtt.on_message()
def handle_mqtt_message(client, userdata, message):
    global img_string 
    global valor_temp1
    
    data = dict(
        topic=message.topic,
        payload=message.payload.decode()
    )
    
    if message.topic == "temperatura":
        valor_temp1 = message.payload.decode()
        
        # Salvando a temperatura em um aquivo de texto
        text_file = open(folder_temp, "w")
        text_file.write(valor_temp1)
        text_file.close()
        
        # quando for imagem em IMAGEM_BASE64
    else:
        # Salvando a mensagem e fazendo o deconder da imagem 
        img_string = message.payload.decode()
        obj_base64.saveStringBin(img_string, "arquivos/imagem_bin")
        time.sleep(5)
        obj_base64.decoder("arquivos/imagem_bin.bin", path_img+file_name_img)
    
   
# Mostrando informações das mensagen recebidas
@mqtt.on_log()
def handle_logging(client, userdata, level, buf):
    print(level, buf)

#%%
@app.route('/home')
def home():
    # Valores grafico de linha do rodapé
    labels_line =  ["Segunda", "Terça", "Quarta", "Quinta", "Sexta", "Sabado", "Domingo"]
    values_line = [37, 39, 30, 29, 26, 31, 40]
    
    #Lendo dos valores de temperatura salvos no aquivo txt
    temp = open(folder_temp, "r")
    valor_temp1 = temp.read()
    valor_temp2 = 100-float(valor_temp1) 
    temp.close()
    

    # Caminho da imagem recebida via MQTT
    full_filename = os.path.join(app.config['UPLOAD_FOLDER'], 'image_mqtt.jpeg')
    
    
    
    # Verfica se o usuario esta logado para poder acessar o index com os graficos
    if 'loggedin' in session:
        
        # usuario logado redireciona para a pagina home com os graficos
        return render_template('index.html', valor_temp1 = int(valor_temp1) , 
                               valor_temp2 = valor_temp2 ,
                               user_image = full_filename, labels_line = labels_line, 
                               values_line = values_line,username=session['username'])
    
    # usuario não logado redireciona para a pagina de login
    return redirect(url_for('login'))




# Execulta o app web
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)