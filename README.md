# Aplicação de sistemas distribuídos com a criação de Dashboard para sensoriamentos com MQTT e Python

## Comunição MQTT


  <a href="https://miro.medium.com/max/875/1*ix27imP2Grk-wd135OY0vA.png">
    <img src="https://miro.medium.com/max/875/1*ix27imP2Grk-wd135OY0vA.png"></a>
    
## Dashboards Interativos com [streamlit](https://www.streamlit.io/).


 <a href="https://miro.medium.com/max/2868/1*o_05kMn2zKOdi0tcgFlgyQ.gif" >
    <img src="https://miro.medium.com/max/2868/1*o_05kMn2zKOdi0tcgFlgyQ.gif"></a>


  1) Instalação de pacotes necessárias:
 
   * Para a execuçãl da aplicação utlizando o MQTT é usado uma maquina linuxi com uma distro Ubuntu server 20.04, com a versão do Python 3.8
   * Para o serviço MQTT é usado o MQTT [mosquito](https://mosquitto.org/), para a instalação use os comandos a baixo.
   ```sh
   $ sudo apt-get update
   $ sudo apt-get install mosquitto
   $ sudo apt-get install mosquitto-clients
   ```
   * Para leitura de temperatura é usado o [ls-sensor](), para a instalação use o comando a baixo.
   ```sh
   $ sudo apt-get install lm-sensors
   ```
   
  2) Instalação de bliotecas Python necessárias:
   * Para a comunicação usando o MQTT com o Python é usado a biblioteca [paho-mqtt](https://www.eclipse.org/paho/index.php?page=clients/python/docs/index.php), para a instalação use o comando a baixo.
   ```sh
   $ pip install paho-mqtt
   ```
   * Para acriação dos Dashboards de monitoramneto é usado a biblioteca [streamlit](https://www.streamlit.io/), para a instalação use o comando a baixo.
   ```sh
   $ sudo pip install streamlit
   ```
 3) Outras bibliotecas usasadas:
  * numpy ```$ pip install numpy ```
  * pandas ```$ pip install pandas ```
  * time ```$ pip install python-time ```
  * subprocess ```$ pip install subprocess.run ```
  * shlex ```$ pip install ushlex```
