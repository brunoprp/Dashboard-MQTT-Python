#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar  4 14:18:16 2021

@author: bruno
"""


import base64 


class ImgEncodDecod64():
    

    def encoder(self, file_img, file_save):
        
        """ 1: Transfoma a imagem em texto com base64
            2: Retorna a string com a imagem codificada 
        """
        # Covertendo para Base64
        with open(file_img , "rb") as image2string: 
            converted_string = base64.b64encode(image2string.read()) 
            image2string.close()
        
        # Salvando o aquivo com .bin  
        with open(file_save+'.bin', "wb") as file:
            file.write(converted_string)
            file.close()
        
        return str(converted_string)[2:] # Retornando a imagem em string
    

        
    def decoder(self, file_bin, file_save):
        """ 
            1: Faz a decodificação do arquivo .bin para a imagem normal
            2: Salva a imagem
        """
        file = open(file_bin, 'rb') 
        byte = file.read() 
        file.close() 
          
        decodeit = open(file_save+'.jpeg', 'wb') 
        decodeit.write(base64.b64decode((byte))) 
        decodeit.close()
        
    
    def saveStringBin(self, string, file_name_save):
        
        """
            1: Recebe uma string e transforma em arquivo .bin
            2: Para fazer a decodificação
        """
        with open(file_name_save+'.bin', "wb") as file:
            file.write(string.encode('ascii'))
            file.close()
        
    
# Criando um objeto da classe ImgEncodDecod64    
#obj_img_base64 = ImgEncodDecod64()
    
# Codificando uma imagem em base64
#string_img = obj_img_base64.encoder('input.jpg', 'imagem_bin')

# Transformando a string em arquivo .bin
#obj_img_base64.saveStringBin(string_img, "teste_save")

# Decodificando a string
#obj_img_base64.decoder("teste_save.bin", "Img_save")


 
    



