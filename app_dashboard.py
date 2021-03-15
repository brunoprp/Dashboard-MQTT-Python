import streamlit as st
import numpy as np
import pandas as pd
import time
from encoder_base64 import ImgEncodDecod64
from PIL import Image
import os
from random import randrange 
import paho.mqtt.client as mqtt


#%% MQTT cominicação

obj_img_base64 = ImgEncodDecod64()
data = ''

def on_message(client, userdata, message):
    print("received message: " ,str(message.payload.decode("utf-8")))
    global data 
    data = str(message.payload.decode("utf-8"))

mqttBroker ="sistemas.amsolution.com.br"

client = mqtt.Client("Smartphone")
client.connect(mqttBroker) 

#%%%

# Add a title
st.title('Monitoramento de Temperatura em tempo real com MQTT')
# Add some text
st.text('Temperatura computador Edvan Viado.')

#%%
# Mostrar todas as temperaturas
chart_data = pd.DataFrame(
    np.random.randn(20, 3),
    columns=['Processador', 'Memoria', 'HD'])

st.line_chart(chart_data)

#%%
# Selecionar a temperartura desejavel
column = st.multiselect(
    'Selecione o Hardware que você deseja monitorar.',
     chart_data.columns)

st.line_chart(chart_data[column])
#%%

# Graficos dinamicos

#status_text = st.sidebar.empty()
#st.sidebar.title("Tempertatura")
#last_rows = np.random.randn(1, 1)
#chart = st.line_chart(last_rows)
#chart2 = st.line_chart(last_rows)


#stop = st.button("Stop")
#cont = 1


image_holder = st.empty()
while True:
    
    
    client.loop_start()
    client.subscribe("IMAGEM_BASE64")
    client.on_message = on_message
    
    # Receder dados do mqttBroker no Canal temperatura por 3 Segundos
    time.sleep(5)
    client.loop_stop()

    # Sanvando a imagem como .bin para decodificar
    save_file_bin = "data_imagem"
    obj_img_base64.saveStringBin(data, "save_file_bin")
    
    # Decoficando a imagem
    name_save_img = "Img_save"
    obj_img_base64.decoder("save_file_bin.bin", name_save_img)
    
    image = Image.open("Img_save.jpg")
    image_holder.image(image, caption='Imagem Recebida pelo MQTT')
    #st.image(image, caption='Imagem sorteada')
    time.sleep(5)
    #cont += 1

    #var = 0.4
    #var = np.array(var).reshape(1,1)
    
    #new_rows = np.random.randn(1, 1).cumsum(axis=0)
    #new_rows2 = np.random.randn(1, 1).cumsum(axis=0)

    #status_text.text("%i Dados Coletados" % cont)
    #chart.add_rows(new_rows)
    #chart2.add_rows(new_rows2)
    #time.sleep(0.5)

    #if stop:
        #df = pd.DataFrame(new_rows2)
        #df.to_csv('out.csv')
    

# Streamlit widgets automatically run the script from top to bottom. Since
# this button is not connected to any other logic, it just causes a plain
# rerun.
#st.button("Re-run")
