#!/usr/bin/env python
# coding: utf-8

# In[11]:


#Importando bibliotecas
from urllib.request import urlopen, urlretrieve, Request
from urllib.error import URLError, HTTPError
from bs4 import BeautifulSoup
import pandas as pd
 
 
#Obtendo o HTML
url = "https://www.fundamentus.com.br/resultado.php"
headers ={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36"}
 
req = Request(url,headers=headers)
response = urlopen(req)
html = response.read()
soup = BeautifulSoup(html,'html.parser')
 
#Obtendo as TAGs de interesse ( topo das informações)
lista =soup.find('table')

#quantidade ações
qtd = soup.findAll('span',class_='tips') 
qtd = range(int(len(qtd)-1)) #retira o ultimo registro para não ter erro
 
#Declarando variáveis cards
resumo = []



# In[12]:


#pega as primeiras informações que não entram no for
papel =  lista.find('td').find('span',class_='tips').getText()
cotacao = lista.find('td').findNext('td').contents[0]
 
for i in qtd:
 
  acoes ={}
 
  PL = cotacao.findNext('td').contents[0]
  PVP = PL.findNext('td').contents[0]
  PSR = PVP.findNext('td').contents[0]
  DividendYied = PSR.findNext('td').contents[0]
  PAtivo = DividendYied.findNext('td').contents[0]
  PCapGiro = PAtivo.findNext('td').contents[0]
  PEbit= PCapGiro.findNext('td').contents[0]
  PAtivoCirc= PEbit.findNext('td').contents[0]
  EVEbit= PAtivoCirc.findNext('td').contents[0]
  EVEbita= EVEbit.findNext('td').contents[0]
  MrgEbit= EVEbita.findNext('td').contents[0]
  MrgLiq= MrgEbit.findNext('td').contents[0]
  LiqCorrente= MrgLiq.findNext('td').contents[0]
  ROIC= LiqCorrente.findNext('td').contents[0]
  ROE= ROIC.findNext('td').contents[0]
  Liq2Meses= ROE.findNext('td').contents[0]
  PatriLiquido= Liq2Meses.findNext('td').contents[0]
  DivBruta_por_Patri= PatriLiquido.findNext('td').contents[0]
  Cresc_5a= DivBruta_por_Patri.findNext('td').contents[0]
 
  acoes['id']= i
  acoes['Papel'] = papel
  acoes['Cotacao'] = cotacao
  acoes['PL'] = PL
  acoes['PVP']=PVP
  acoes['DividendYied']=DividendYied
  acoes['PAtivo']=PAtivo
  acoes['PCapGiro']=PCapGiro
  acoes['PEbit']=PEbit
  acoes['PAtivoCirc']=PAtivoCirc
  acoes['EVEbit']=EVEbit
  acoes['EVEbita']=EVEbita
  acoes['MrgEbit']=MrgEbit
  acoes['MrgLiq']=MrgLiq
  acoes['LiqCorrente']=LiqCorrente
  acoes['ROIC']=ROIC
  acoes['ROE']=ROE
  acoes['Liq2Meses']=Liq2Meses
  acoes['PatriLiquido']=PatriLiquido
  acoes['DivBruta_por_Patri']=DivBruta_por_Patri
  acoes['Cresc_5a']=Cresc_5a
 
  #Adiciona o dicionário de ações em uma lista
  resumo.append(acoes)
 
  #try retorna erro por a ultima linha não encontra o span
  try:
    papel = Cresc_5a.findNext('td').span.a.contents[0]
    cotacao = papel.findPrevious('td').findNext('td').contents[0]
 
  except HTTPError as e:
    print(e.status, e.reason)


# In[13]:


#cria data frame (Pré visualização)
dataset = pd.DataFrame(resumo)
 
dataset.head(5000)


# In[14]:


#TRATAMENTO DE DADOS CAMPO PL  
dataset['PL'] = dataset['PL'].str.replace('.', '', regex=True).replace(',', '.', regex=True)
convert_dict = {'PL': float}
dataset['PL']  = dataset['PL'].astype(convert_dict)
 
#TRATAMENTO DE DADOS CAMPO ROE
dataset['ROE'] = dataset['ROE'].str.replace('.', '', regex=True).replace(',', '.', regex=True).replace('%', '', regex=True)
convert_dict = {'ROE': float}
dataset['ROE']  = dataset['ROE'].astype(convert_dict)/100
 
#TRATAMENTO DE DADOS CAMPO MrgLiq
dataset['MrgLiq'] = dataset['MrgLiq'].str.replace('.', '', regex=True).replace(',', '.', regex=True).replace('%', '', regex=True)
convert_dict = {'MrgLiq': float}
dataset['MrgLiq']  = dataset['MrgLiq'].astype(convert_dict)/100
 
#TRATAMENTO DE DADOS CAMPO DIVIDA BRUTA/PATRIMONIO  
dataset['DivBruta_por_Patri'] = dataset['DivBruta_por_Patri'].str.replace('.', '', regex=True).replace(',', '.', regex=True)
convert_dict = {'DivBruta_por_Patri': float}
dataset['DivBruta_por_Patri']  = dataset['DivBruta_por_Patri'].astype(convert_dict)
 
#TRATAMENTO DE DADOS CAMPO CAGER
dataset['Cresc_5a'] = dataset['Cresc_5a'].str.replace('.', '', regex=True).replace(',', '.', regex=True).replace('%', '', regex=True)
convert_dict = {'Cresc_5a': float}
dataset['Cresc_5a']  = dataset['Cresc_5a'].astype(convert_dict)/100
 
#TRATAMENTO DE DADOS DIVIDEND YIED
dataset['DividendYied'] = dataset['DividendYied'].str.replace('.', '', regex=True).replace(',', '.', regex=True).replace('%', '', regex=True)
convert_dict = {'DividendYied': float}
dataset['DividendYied']  = dataset['DividendYied'].astype(convert_dict)/100
 
#TRATAMENTO DE DADOS CAMPO ROIC
dataset['ROIC'] = dataset['ROIC'].str.replace('.', '', regex=True).replace(',', '.', regex=True).replace('%', '', regex=True)
convert_dict = {'ROIC': float}
dataset['ROIC']  = dataset['ROIC'].astype(convert_dict)/100
 
#TRATAMENTO DE DADOS CAMPO ROIC
dataset['MrgEbit'] = dataset['MrgEbit'].str.replace('.', '', regex=True).replace(',', '.', regex=True).replace('%', '', regex=True)
convert_dict = {'MrgEbit': float}
dataset['MrgEbit']  = dataset['MrgEbit'].astype(convert_dict)/100
 
#TRATAMENTO DE DADOS CAMPO PVP  
dataset['PVP'] = dataset['PVP'].str.replace('.', '', regex=True).replace(',', '.', regex=True)
convert_dict = {'PVP': float}
dataset['PVP']  = dataset['PVP'].astype(convert_dict)
 
#TRATAMENTO DE DADOS CAMPO EVEbit 
dataset['EVEbit'] = dataset['EVEbit'].str.replace('.', '', regex=True).replace(',', '.', regex=True)
convert_dict = {'EVEbit': float}
dataset['EVEbit']  = dataset['EVEbit'].astype(convert_dict)
 
#TRATAMENTO DE DADOS CAMPO EVEbita
dataset['EVEbita'] = dataset['EVEbita'].str.replace('.', '', regex=True).replace(',', '.', regex=True)
convert_dict = {'EVEbita': float}
dataset['EVEbita']  = dataset['EVEbita'].astype(convert_dict)


# In[15]:


#Gera uma tabela com os dados do DataFrame
pd_df = dataset
nome_arquivo = "acoes.xlsx"
# Salvar o DataFrme em um arquivo Excel
dataset.to_excel(nome_arquivo, index=False)

