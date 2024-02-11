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



url_mapa= 'https://raw.githubusercontent.com/tbrugz/geodata-br/master/geojson/geojs-100-mun.json'

def importa_geo():
    mapa = pd.read_json(url_mapa)
    print(mapa.head())
    return mapa

with urlopen(url_mapa) as response:
    counties = json.load(response)

importa_geo()
dados[' Valor '].info()

fig = px.choropleth_mapbox(dados, geojson=mapa, color=' Valor ',
                           color_continuous_scale="Viridis",
                           range_color=(0, 12),
                           mapbox_style="carto-positron",
                           zoom=3, center = {"lat": 37.0902, "lon": -95.7129},
                           opacity=0.5,
                           labels={'unemp':'unemployment rate'}
                          )
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

fig.show()

print('FInal')

