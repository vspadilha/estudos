import pandas as pd
import streamlit as st
import numpy as np
import plotly.express as px
import locale
import time
from dash import Dash
from dash.dash_table.Format import Format, Group
#from dash import DiskcacheManager
import json
#import geopandas as gpd
#import diskcache

#Configurações
locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

my_bar = st.progress(0.0, text='')

#cache = diskcache.Cache("./cache")
#background_callback_manager = DiskcacheManager(cache)

#Configurações
st.title('Estudo de caso sobre o Metrô no RS e Mobilidade', anchor='Home')

#Importar Dados

#url='datasets/Dados Domicilios 2024/43_RS.zip'
#url='c:/Users/VitorS/OneDrive/Python/Streamlit/Análise de Alugueis/datasets/Dados Domicilios 2024/43_RS.zip'
url='datasets/dados_metro_rv2.parquet'
url_cidades='datasets/Dados Domicilios 2024/lista_cidades.csv'

@st.cache_data
def importa_dados():
    df = pd.read_parquet(url)
    return df

@st.cache_data
def importa_cidades():
    lista_cidades = pd.read_csv(url_cidades, sep=';', encoding='ISO-8859-1')
    return lista_cidades


df = importa_dados()


lista_cidades= importa_cidades()
lista_cidades['Código Município Completo'].unique()

dict_cidade = dict(lista_cidades)
dict_cidade = dict(zip(lista_cidades['Nome_Município'], lista_cidades['Código Município Completo']))

#nome_cidade = st.selectbox('Selecione a Cidade', list(dict_cidade.keys()), index=0)

# Adicionar um seletor para escolher o nome das cidades (multiselect)
nomes_cidades = st.multiselect('Selecione o nome das cidades:', options=list(dict_cidade.keys()), default=['São Leopoldo', 'Novo Hamburgo', 'Canoas', 'Esteio', 'Sapucaia do Sul', 'Porto Alegre'])
#nomes_cidades = st.multiselect('Selecione o nome das cidades:', options=list(dict_cidade.keys()), default=['São Leopoldo', 'Novo Hamburgo'])

st.write(nomes_cidades)

# Mostrar os códigos dos municípios correspondentes aos nomes das cidades selecionadas
if nomes_cidades:
    codigos_municipios = [dict_cidade[nome_cidade] for nome_cidade in nomes_cidades]
    st.write('Os códigos dos municípios selecionados são:', codigos_municipios)
    
    # Filtrar o DataFrame com base nos códigos dos municípios selecionados
    df_filtered = df[df['COD_MUN'].isin(codigos_municipios)]
    
    # Exibir o DataFrame filtrado
    st.write(df_filtered.head())
else:
    st.write('Nenhuma cidade selecionada.')

st.write(df_filtered['COD_MUN'].value_counts())

#Limpar Dados



#Mostrar Dados



#Sandbox

select_cores = 'pubu'
tamanho_maximo = st.slider('Distancia Máxima em KM', 1,3)

df_menor_distancia = df_filtered[df_filtered['Menor_Distancia_Entre_Colunas']<= tamanho_maximo]

st.write(df_menor_distancia['COD_MUN'].value_counts())

fig_map = px.scatter_mapbox(df_menor_distancia, lat='LATITUDE', lon='LONGITUDE',
                                zoom = 11,
                                color='COD_ESPECIE',
                                size='Menor_Distancia_Entre_Colunas',
                                #hover_name='COD_ESPECIE',
                                #center = {"lat":-30.03787737004909, "lon": -51.21334191009066},
                                opacity = 0.4,
                                color_continuous_scale='blues',
                                color_continuous_scale=select_cores,
                                mapbox_style='carto-darkmatter',
                                height=1080,
                                width=800,
                                size_max=1.5,
                                title='Mapa com Estudo sobre mobilidade das pessoas até o Trensurb',
                                #animation_group='COD_ESPECIE',
                                #animation_frame='COD_ESPECIE',
                                hover_data=['Menor_Distancia_Entre_Colunas'],
                                )


  

st.write(fig_map)

st.divider()



#df_filtered.memory_usage()
#df_filtered.info()




