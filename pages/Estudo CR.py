import pandas as pd
import streamlit as st
import time
import numpy as np
import plotly.express as px
import locale

#Configurações
locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')


#Importação de Dados

@st.cache_data
def import_data():
    dados = pd.read_excel('datasets/dados_cr.xlsx')
    return dados

dados = import_data()

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
    
  

    df.info()
    return df

df = clean_data()


# Gráficos
st.title('Estudo de Caso Imobiliária')

st.subheader('Le Dataframe')
st.dataframe(df)
st.caption('Dados extraídos da internet')
st.header('Mostrando os imóveis no Mapa')

with st.container():
    st.map(df, size=0.5, color=[0, 255, 255])
    st.caption('Dados distribuidos sem nenhum tratamento, apenas lat e lon via MapBox')
st.divider()

##Filtros para remover outros status
filtered_df = df[(df['Status'] == 'Novo') | (df['Status'] == 'Dispon¡vel')]
range_valores = st.slider('Selecione Valores', 0, int(filtered_df['Valor'].max()), 15000)
filtered_df = filtered_df[(filtered_df['Valor'] > 300) & (filtered_df['Valor'] < range_valores)]
filtered_df['Valor'].count()

with st.container(border=True):
    media = np.mean(filtered_df["Valor"])
    std = np.std(filtered_df['Valor'])
    mediana = np.median(filtered_df['Valor'])
    
    #Colunas com as Médias
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Média", f'{locale.currency(media, grouping=True)}')
    col2.metric(f"Desvio Padrão", f'{locale.currency(std, grouping=True)}')
    col3.metric("Mediana", f'{locale.currency(mediana, grouping=True)}')

hist = px.histogram(filtered_df, x='Valor', height=400)

hist


teste = filtered_df.copy()

teste['CreatedAt'] = pd.to_datetime(teste['CreatedAt'])
teste['Mes'] = teste['CreatedAt'].dt.month
teste['Year'] = teste['CreatedAt'].dt.year

teste2 = pd.DataFrame(teste.groupby('Mes').count())
teste2.reset_index(inplace=True)

colunas = st.selectbox('Filtrar por Colunas no DF', filtered_df.columns, index=4)

st.scatter_chart(filtered_df, x='Valor', y=colunas)