import pandas as pd
import streamlit as st
import numpy as np


#Configurações

st.set_page_config(
    page_title="Dados, Mapas e outros estudos com Python",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://www.extremelycoolapp.com/help',
        'Report a bug': "https://www.extremelycoolapp.com/bug",
        'About': "# This is a header. This is an *extremely* cool app!"
    }
)


#Importação de Dados

#Limpeza de Dados


#Sidebar


#Title

col1, col2 = st.columns([3,12])
    
with col1:
        with st.container(border=True):
                st.image('https://docs.streamlit.io/logo.svg', use_column_width=True, clamp=False)
with col2:
        st.header('Vítor S. Padilha - Analista de dados')
        st.subheader('Tentando analisar uns dados, aí pelo mundo')



st.write('---')

#Gráficos
st.header("Header 1")

st.write('---')

