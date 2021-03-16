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

app = Flask(__name__)

@app.route("/chart_donut")
def chart():
    labels =['good', 'mediocre','bad']
    values = [30, 10, 12]
    
    
    return render_template('chart_donut.html', values=values,labels=labels)




if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)