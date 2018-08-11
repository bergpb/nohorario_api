# -*- coding: utf-8 -*-
import os
import re
import json
import pandas as pd
from bs4 import BeautifulSoup
from flask import Flask, jsonify, request
from urllib.request import urlopen, Request

#https://medium.com/@ageitgey/quick-tip-the-easiest-way-to-grab-data-out-of-a-web-page-in-python-7153cecfca58


app = Flask(__name__)


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
  
  
@app.route('/api', methods=['GET'])

def retornaLinhaEspecifica():
    # tentando usar o pandas
    html_doc = urlopen("https://www.evitoria.com.br/linhas-e-horarios/363_2-cumbuco-via-mr-hull").read()
    soup = BeautifulSoup(html_doc, "html.parser")
    content = soup.find("table", class_="table table-bordered table-hover")
    
    calls_df = pd.read_html(content, header=0)

    print(calls_df)
    
    return jsonify(status="ok")
    

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
