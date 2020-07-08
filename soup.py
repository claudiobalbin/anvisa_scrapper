import pandas as pd
import requests
from bs4 import BeautifulSoup


cd_reg_anvisa = 8003400014

print('Iniciando navegador')
url = 'https://consultas.anvisa.gov.br/#/saude/q/?numeroRegistro={}'.format(cd_reg_anvisa)

req = requests.get(url)
if req.status_code == 200:
    print('Requisição bem sucedida!')
    content = req.content

soup = BeautifulSoup(content, 'html.parser')
reg_anvisa = soup.find(value=cd_reg_anvisa)

print('Procedimento concluido')