# -*- coding: utf-8 -*-
import os
import re
import json
import pandas as pd
from bs4 import BeautifulSoup
from urllib.request import urlopen, Request

def retornaLinhaEspecifica():
    tables_array = []
    html_doc = urlopen("https://www.evitoria.com.br/linhas-e-horarios/363_2-cumbuco-via-mr-hull").read()
    soup = BeautifulSoup(html_doc, "html.parser")
    content = soup.find("table", class_="table table-bordered table-hover")

    for i in range(0, 3):
        if (i == 0 or i == 2):
            calls_df = pd.read_html(str(content), header = 0)
            df = calls_df[0].iloc[:, i]
            tables_array.append(df.to_json(orient='records')[1:-1].replace('},{', '} {'))

    print (tables_array)


retornaLinhaEspecifica()
