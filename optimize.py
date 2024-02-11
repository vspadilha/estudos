import pandas as pd
from urllib.request import urlopen
import json
import plotly.express as px

dados = pd.read_excel('datasets/dados_cr.xlsx')

dados.info()


dados['State'] = dados['State'].astype('category')



dados['Status'].value_counts()


dados['Status'] = dados['Status'].replace('Dispon¡vel' , 'Disponivel')
dados['Status'] = dados['Status'].replace('Indispon¡vel' , 'indisponivel')


contagem = dados['Status'].value_counts()

val1000 = contagem[contagem > 1000].index.tolist()

df2 = dados[(dados['Status'] == 'Novo')]

df2['Status'].value_counts()
dados['Status'].value_counts()

df2.to_parquet('dados.parquet.gzip', compression='gzip')

dfp = pd.read_parquet("dados.parquet.gzip")

dfp.info()

dfp['Tipo'] = dfp['Tipo'].astype('category')
dfp['Status'] = dfp['Status'].astype('category')
dfp['State'] = dfp['State'].astype('category')



