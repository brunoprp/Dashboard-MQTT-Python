import streamlit as st
import numpy as np
import pandas as pd
import time
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

status_text = st.sidebar.empty()
st.sidebar.title("Tempertatura")
last_rows = np.random.randn(1, 1)
chart = st.line_chart(last_rows)
chart2 = st.line_chart(last_rows)


stop = st.button("Stop")
cont = 1


while True:
    cont += 1

    #var = 0.4
    #var = np.array(var).reshape(1,1)
    
    new_rows = np.random.randn(1, 1).cumsum(axis=0)
    new_rows2 = np.random.randn(1, 1).cumsum(axis=0)

    status_text.text("%i Dados Coletados" % cont)
    chart.add_rows(new_rows)
    chart2.add_rows(new_rows2)
    time.sleep(0.5)

    if stop:
        break

# Streamlit widgets automatically run the script from top to bottom. Since
# this button is not connected to any other logic, it just causes a plain
# rerun.
st.button("Re-run")
