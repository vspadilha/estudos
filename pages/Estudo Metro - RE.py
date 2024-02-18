import pandas as pd
import streamlit as st
import plotly.express as px
import locale
import time
from dash import Dash
from dash.dash_table.Format import Format, Group


#Configurações
locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

st.set_page_config(
    page_title="Dados, Mapas e outros estudos com Python",
    page_icon="🧊",
    layout='centered',
    initial_sidebar_state="auto",
    menu_items={
        'Get Help': 'https://linkedin.com/in/vspadilha',
        'Report a bug': "https://linkedin.com/in/vspadilha",
        'About': "Me ache no LinkedIn https://linkedin.com/in/vspadilha =)"
    }
)

#Título
st.title('Estudo de caso sobre o Metrô no RS e Mobilidade', anchor='Home')
my_bar = st.progress(0.0, text='')
#Importar Dados

url='datasets/dados_domiciolios_otimizado.parquet'
url_cidades='datasets/Dados Domicilios 2024/lista_cidades.csv'

@st.cache_data
def importa_dados():
    df = pd.read_parquet(url)
    return df

@st.cache_data
def importa_cidades():
    lista_cidades = pd.read_csv(url_cidades, sep=';', encoding='ISO-8859-1')
    return lista_cidades


##Tempo de carregamento e Memória do DF
my_bar.progress(0, 'Carregamento')
t_ini = time.time()

df = importa_dados()
st.write(url)
lista_cidades= importa_cidades()

t_fim = time.time()
tempo_total = (t_fim - t_ini)*1000
my_bar.progress(100, f'Carregamento do DataFrame em {tempo_total:.2f} ms')

memory_usage = df.memory_usage(deep=True).sum() / (1024 * 1024)  # Convert bytes to MB
st.text(f'Uso da memório: {memory_usage:.2f} mb')

#Cria um dict com Nome do Município e respectivo Código do IBGE
dict_cidade = dict(lista_cidades)
dict_cidade = dict(zip(lista_cidades['Nome_Município'], lista_cidades['Código Município Completo']))

menu_lateral = st.sidebar
with menu_lateral:
    # Adicionar um seletor para escolher o nome das cidades (multiselect)
    nomes_cidades = st.multiselect('Selecione o nome das cidades:', options=list(dict_cidade.keys()), default=['São Leopoldo', 'Novo Hamburgo', 'Canoas', 'Esteio', 'Sapucaia do Sul', 'Porto Alegre'])
    cores_mapa = st.radio('Seletor de Cores: ', ['blues','spectral', 'geyser'])
    bolotas = st.radio('Tamanho Bolotas: ',[1,2,3] )
    
# Mostrar os códigos dos municípios correspondentes aos nomes das cidades selecionadas
if nomes_cidades:
    codigos_municipios = [dict_cidade[nome_cidade] for nome_cidade in nomes_cidades]
    #st.write('Os códigos dos municípios selecionados são:', codigos_municipios)
    
    # Filtrar o DataFrame com base nos códigos dos municípios selecionados
    df_filtered = df[df['COD_MUN'].isin(codigos_municipios)]
    
    # Exibir o DataFrame filtrado
    with st.expander('Preview do DataFrame'):
        st.write(df_filtered.head())
else:
    st.write('Nenhuma cidade selecionada.')


#Sandbox

#Tamanho máximo das bolotas
tamanho_maximo = 1.1
df_menor_distancia = df_filtered[df_filtered['Menor_Distancia_Entre_Colunas']<= tamanho_maximo]

#Atualiza a coluna size para que todos fiquem do mesmo tamanho
df_menor_distancia['size'] = df_menor_distancia['Menor_Distancia_Entre_Colunas']+0.8

fig_map = px.scatter_mapbox(df_menor_distancia, lat='LATITUDE', lon='LONGITUDE',
                                zoom = 10,
                                color='COD_ESPECIE',
                                size='size',
                                #hover_name='COD_ESPECIE',
                                #center = {"lat":-30.03787737004909, "lon": -51.21334191009066},
                                opacity = 0.3,
                                color_continuous_scale=cores_mapa,
                                mapbox_style='carto-darkmatter',
                                height=800,
                                width=800,
                                size_max=bolotas,
                                title=f'Mapa mostrando residências no raio de {tamanho_maximo} km',
                                                                                               
                                )




st.write(fig_map)


st.dataframe(df_filtered['Nome_Municipio'].value_counts(), column_config={
    'count': st.column_config.NumberColumn('Contagem', step=1)
})
st.write(df_menor_distancia['Nome_Municipio'].value_counts())

st.write(
    (df_menor_distancia['Nome_Municipio'].value_counts() / df_filtered['Nome_Municipio'].value_counts())
    )

st.write(df_menor_distancia['COD_ESPECIE'].value_counts())

st.divider()
st.caption('Criado e desenvolvido por Vítor S. Padilha, 2024.')
st.caption('https://ftp.ibge.gov.br/Cadastro_Nacional_de_Enderecos_para_Fins_Estatisticos/Censo_Demografico_2022/Coordenadas_enderecos/')
#df_filtered.memory_usage()
#df_filtered.info()






