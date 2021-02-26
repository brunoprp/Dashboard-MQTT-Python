#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 25 16:13:13 2021
servidor: sistemas.amsolution.com.br 
    porta SSH: 10000
     usuario: administrador
     senha: vo5uew#eiL

@author: bruno
"""
import subprocess
import shlex

def measureTemp():
    """sudo apt-get install lm-sensors"""
    temp = subprocess.Popen(shlex.split('sensors -u'),
                                stdout=subprocess.PIPE,
                                bufsize=10, universal_newlines=True)

    return temp.communicate()[0].split()[8]

