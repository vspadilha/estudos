import pandas as pd
import streamlit as st
import numpy as np
import plotly.express as px
import locale
import time
from dash import Dash
from dash.dash_table.Format import Format, Group
import json



#Configurações
locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
#locale.setlocale(locale.LC_ALL, '')

my_bar = st.progress(0, text='')


#Importação de Dados

@st.cache_data
def import_data():
    dados = pd.read_parquet("datasets/dados.parquet.gzip") 
    return dados

my_bar.progress(0, 'Carregamento')
t_ini = time.time()
dados = import_data()
t_fim = time.time()
tempo_total = (t_fim - t_ini)*1000
my_bar.progress(100, f'Carregamento do DataFrame em {tempo_total:.2f} ms')
memory_usage = dados.memory_usage(deep=True).sum() / (1024 * 1024)  # Convert bytes to MB
st.text(f'Uso da memório: {memory_usage:.2f} mb')

#dados.info()

#Limpeza de Dados
@st.cache_data
def clean_data():
    df = dados.loc[dados['Latitude'].notna()]
    df = df.loc[dados['Latitude'].notnull()]
    
    #Mudando os nomes das colunas para o st.map entender
    df = df.rename(columns={'Latitude' : 'LAT', 'Longitude': 'LON'} ) 
    
    #Coluna Valor estava com espaços
    df = df.rename(columns={' Valor ' : 'Valor'} )
    df['Valor_Correto'] = pd.to_numeric(df['Valor'])
    
    #Filtrar somente porto alegre
    

    df.info()
    return df

df = clean_data()

# Gráficos
st.title('Estudo de Caso - Dados de Imóveis')

st.subheader('Le Dataframe')
st.dataframe(df.head())
st.caption('Dados extraídos da internet')

st.header('Mostrando os imóveis no Mapa')
st.text('Navegue pelos dados dos imóveis para aluguel e sua distribuição por lat e lon')
with st.container():
    df.loc[df.Valor > 15000, 'Valor'] = 15000
    st.map(data=df, size=40, color=[0, 250, 255, 0.1])
    st.caption('Dados distribuidos sem nenhum tratamento, apenas lat e lon via MapBox')
st.divider()

##Filtros para remover outros status

st.header('Indicadores Básicos')

filtered_df = df[(df['Status'] == 'Novo') | (df['Status'] == 'Dispon¡vel')]
range_valores = st.slider('Selecione o valor MAX do aluguel para atualizar as médias', 0, int(filtered_df['Valor'].max()),int(filtered_df['Valor'].max()))
filtered_df = filtered_df[(filtered_df['Valor'] > 200) & (filtered_df['Valor'] < range_valores)]
filtered_df['Valor'].count()

with st.container(border=True):
    media = np.mean(filtered_df["Valor"])
    std = np.std(filtered_df['Valor'])
    mediana = np.median(filtered_df['Valor'])
    qtd =  len(filtered_df['Name'])
    
    #Colunas com as Médias
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric('Quantidade', f'{qtd:n}')
    col2.metric("Média", f'{locale.currency(media, grouping=True)}')
    col3.metric(f"Desvio Padrão", f'{locale.currency(std, grouping=True)}')
    col4.metric("Mediana", f'{locale.currency(mediana, grouping=True)}')
    
    # Gambi para arrumar quando o Locale estava sem funcionar.
    #col2.metric("Média", f'{media:n}')
    #col3.metric(f"Desvio Padrão", f'{std:n}')
    #col4.metric("Mediana", f'{mediana:n}')

hist = px.histogram(filtered_df, x='Valor', height=400)

hist

# Area de Testes
st.divider()

filtered_df['Status'] = filtered_df['Status'].astype('category')
#filtered_df = filtered_df.drop('Name', axis=1)
filtered_df = filtered_df.drop('Valor_Correto', axis=1)
filtered_df['Tipo'] = filtered_df['Tipo'].astype('category')
filtered_df['State'] = filtered_df['State'].astype('category')

selecao = st.selectbox('Selecione a Linha de Tendencia:',['lowess', 'rolling', 'ewm', 'expanding', 'ols'])
fig = px.scatter(filtered_df, x='CreatedAt', y='Valor', trendline=selecao)

fig


#fig2 = px.choropleth_mapbox(data_frame=filtered_df, locations='State', labels=True)

#importa_geo()

st.divider()

st.subheader('Mapa usando o Plotly "px.scatter_mapbox"')
st.text('Aqui tendo a lat e lon como valores, fica relativamente fácil implementar com um visual mais bonito.')

colorscales = px.colors.named_colorscales()
select_cores = st.radio('Cores: ', colorscales, 4, horizontal=True)


fig_map = px.scatter_mapbox(filtered_df, lat='LAT', lon='LON',
                                zoom = 12,
                                color='Valor',
                                size='Valor',
                                hover_name='Name',
                                center = {"lat":-30.03787737004909, "lon": -51.21334191009066},
                                opacity = 0.4,
                                #color_continuous_scale='blues',
                                color_continuous_scale=select_cores,
                                mapbox_style='carto-darkmatter',
                                height=1080,
                                width=1080,
                                size_max=13,
                                title='Mesmo pada de Cima, só que bonito',
                                #animation_group='Status',
                                #animation_frame='LAT',
                                                                
                                )




st.write(fig_map)

#filtered_df.info()

st.divider()

