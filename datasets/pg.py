import pandas as pd
import streamlit as st

st.header('Playground')


df = pd.read_csv('datasets/da_imoveis_202307.csv', encoding='ISO-8859-1', sep=';')

df1 = pd.read_csv('C:/Users/VitorS/OneDrive/Python/Streamlit/Análise de Alugueis/datasets/DA_Imoveis_202307.csv', sep=';', encoding='ISO-8859-1') 


df1.head(1).T


df1.info()

df1.describe().T

df1['Tipo Imóvel'].value_counts()



# Contar o número de ocorrências de cada tipo de imóvel
contagem_tipo_imovel = df1['Tipo Imóvel'].value_counts()
contagem_UF = df1['UF'].value_counts()



# Filtrar o DataFrame com base na contagem
df = df.loc[df['Tipo Imóvel'].isin(contagem_tipo_imovel[contagem_tipo_imovel > 500].index)]
df = df.loc[df['UF'].isin(contagem_UF[contagem_UF > 500].index)]

df['Data_Cad'] = df.to_timestamp(df['Data de cadastramento'])

df.info()
df1.info()


df['Tipo Imóvel'] = df['Tipo Imóvel'].astype('category')

df['UF'].count()


df['UF'] = df['UF'].astype('category')

df['Número do RIP'] = df['Número do RIP'].astype('int64')

df.columns


#Ler o Arquivo novo
df2 = pd.read_parquet('ddd2.parquet')

df2['Data de cadastramento'] = pd.to_datetime(df2['Data de cadastramento'], errors='coerce')

def save_file():
    df2.to_parquet('ddd2.parquet')
    df2 = pd.read_parquet('ddd2.parquet')
    return df2

save_file()
df2.head(5).T
df2.loc[df2['Data de cadastramento'].notna().value_counts()]

df2.reset_index(inplace=True)

df2.info()
df2.memory_usage()

df2['Área da União'] = df2['Área da União'].astype('float64')

df2['AU'] = pd.to_numeric(df2['Área da União'])

df2['Valor N'] = pd.to_numeric(df2['Valor N'], errors='coerce')

df2['Valor N'] = df2['Valor N'].str.replace('.', '').str.replace(',', '.')

df2

colunas_object = df2.select_dtypes(include='object').columns
print(colunas_object)