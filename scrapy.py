# -*- coding: utf-8 -*-
import os
import re
import csv
import json
import pandas as pd
from flask_cors import CORS
from bs4 import BeautifulSoup
from flask import Flask, jsonify, request
from urllib.request import urlopen, Request

#https://medium.com/@ageitgey/quick-tip-the-easiest-way-to-grab-data-out-of-a-web-page-in-python-7153cecfca58

app = Flask(__name__)

CORS(app, resources={r"/api/*": {"origins": "*"}})

@app.route('/api/rotas', methods=['GET'])

def retornaTodas():
  i = 0
  json = []

  html_doc = urlopen("https://www.evitoria.com.br/linhas-e-horarios").read()

  soup = BeautifulSoup(html_doc, "html.parser")

  for dataBox in soup.find_all("div", class_="col-md-3 col-sm-6 m-b10 filtr-item"):
    link = dataBox.find("a")["href"]
    nome = dataBox.find("h5", class_="text-white").text

    json.append({
        'id': i,
        'nome_linha': nome,
        'link_linha': 'https://www.evitoria.com.br'+link
    })

    i += 1

  return jsonify(rotas=json)
  
  
@app.route('/api/<nome_linha>/<dia>', methods=['GET'])

def retornaLinha(nome_linha, dia):
    dataframe = pd.ExcelFile(nome_linha+'.xls')
    sheets = dataframe.sheet_names
    df = pd.read_excel(dataframe, dia)
    horarios_linha = df.to_json(orient='records')
    
    # esse for retorna todas as abas do excel
    #for i in range(0, len(sheets)):
    #    df = pd.read_excel(dataframe, sheets[i])
    #    horarios_linha.append({
    #        horarios_linha[sheets[i]]: df.to_json(orient='records')
    #    })
    
        
        
    return(horarios_linha)
    
    
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
