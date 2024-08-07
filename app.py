import streamlit as st
import pandas as pd
import numpy as np
import requests
import io
#importar função de uma pasta no nível acima
import sys
import os
import openpyxl

st.set_page_config(
    page_title="Acompanhameto de Produtos",
    page_icon="💎",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.header("Acompanhamento de Produtos Shopify", divider="blue")

df = pd.read_excel('arquivos/dados_prods_.xlsx')

col4, col5, col6 = st.columns([1, 1, 1])

df = df[df['totalInventory'] > 0]
df_total = df.shape[0]
df_descricao = df[df['descriptionHtml'].isnull()]
df_imagem = df[df['mediaCount.count'] == 0]
df_composicao = df[df['metafield.value'].isnull()]
df_descricao = df_descricao.shape[0]
df_imagem = df_imagem.shape[0]
df_composicao = df_composicao.shape[0]

rel_desc = df_descricao / df_total * 100 * -1
rel_desc = round(rel_desc, 2)
rel_desc = str(rel_desc) + "%"

rel_imag = df_imagem / df_total * 100 * -1
rel_imag = round(rel_imag, 2)
rel_imag = str(rel_imag) + "%"

rel_comp = df_composicao / df_total * 100 * -1
rel_comp = round(rel_comp, 2)
rel_comp = str(rel_comp) + "%"

col4, col5, col6 = st.columns([1, 1, 1])
with col4:
    container = st.container(border=True)
    with container:
        st.metric("Quantidade de produtos sem descrição:", df_descricao, rel_desc)

with col5:
    container = st.container(border=True)
    with container:
        st.metric("Quantidade de produtos sem imagem:", df_imagem, rel_imag)
with col6:
    container = st.container(border=True)
    with container:
        st.metric("Quantidade de produtos sem composição:", df_composicao, rel_comp)

container = st.container(border=True)
with container:
    col1, col2, col3 = st.columns([1, 1, 1])



colunas_comuns = [
    "sku", 
    "title",
    "Colecao",
    "Desc. Gr.",
    "Desc. Subgr.",
    # "Desc. Produto",
    # "Markup Aplic",
    # "Pr. Custo",
    "Pr Venda unit",
    # "Faixa de Preco",
    # "Gde. Gr.",
    # "Metal",
    # "Cor Padrao",
    "Desc Cor"
]

colecoes = [
    "Todas",
    "15 anos JV",
    "CHOKER AMORE",
    "AVANT GARDE",
    "BLACK LEOPARDO",
    "BLOSSOM (MAES 2020)",
    "BRASIL",
    "CELEBRATE",
    "CHAIN",
    "CHAIN LOVERS",
    "COLEÇÃO CHOKER",
    "DECO",
    "CLÁSSICO",
    "VOCE",
    "ESPECIAL",
    "ETERNA ROCK",
    "GALA NATAL 2013",
    "COLEÇÃO GALERIA",
    "FETICHE",
    "FIRST DIAMOND",
    "PEQUENO PRINCIPE",
    "PARCERIA INSTITUTO PROTEA",
    "LEOPARDO",
    "LOVE NY",
    "LIFE STYLE",
    "ORQUIDEA",
    "PISCINE",
    "PURA",
    "TOU LES JOUR",
    "RIVIERA",
    "VITA ETERNA",
    "SAVAGE",
    "VOYEUR",
    "COLEÇÃO UNIVERSO",
    "WHITE CHAIN",
    "WE LOVE SAPPHIRE",
    "POP CHAIN",
    "ROCK & HOT",
    "ROCK STAR",
    "COLEÇÃO POP",
    "MARE",
    "DOLCE VITA",
    "JV MAN II 2019",
    "ROCK CHAIN",
    "JV MAN",
    "LETRA",
    "COLEÇÃO MÃES 2013",
    "COLEÇÃO NAMORADOS 2012",
    "TROPICAL",
    "I DON'T CARE",
    "NEW VINTAGE",
]

    

with col1:

    option = st.selectbox("Selecione a opção desejada:", ["Produtos sem descrição", "Produtos sem imagem", "Produtos sem composição"])




if option == "Produtos sem descrição":

    st.subheader("Produtos sem descrição:")
    
    df = df[df['descriptionHtml'].isnull()]
    #contar a quantidade de produtos sem descri
    qtd_produtos = df.shape[0]
    df = df[colunas_comuns]
    df = df.rename(columns={'sku': 'SKU', 'title': 'Título'})
    df = df.reset_index(drop=True)
    
    colecoes_filt = df['Colecao'].unique().tolist()
    colecoes_filt.insert(0, "Todas")
    
    with col2:
        option2 = st.selectbox("Selecione a coleção desejada:", colecoes_filt)
    
    if option2 != "Todas":
        df = df[df['Colecao'] == option2]
    st.dataframe(df)
    
elif option == "Produtos sem imagem":
    
    st.subheader("Produtos sem Imagem:")
    
    df = df[df['mediaCount.count'] == 0]
    qtd_imagens = df.shape[0]
    df = df[colunas_comuns]
    df = df.rename(columns={'mediaCount.count': 'Imagens', 'sku': 'SKU', 'title': 'Título'})
    df = df.reset_index(drop=True)
    
    colecoes_filt = df['Colecao'].unique().tolist()
    colecoes_filt.insert(0, "Todas")
    
    with col2:
        option2 = st.selectbox("Selecione a coleção desejada:", colecoes_filt)
        
    if option2 != "Todas":
        df = df[df['Colecao'] == option2]
    st.dataframe(df)
    
elif option == "Produtos sem composição":
    
    st.subheader("Produtos sem Composição:")
    
    df = df[df['metafield.value'].isnull()]
    qtd_composicao = df.shape[0]
    df = df[colunas_comuns]
    df = df.rename(columns={'metafield.value': 'Composição', 'sku': 'SKU', 'title': 'Título'})
    df = df.reset_index(drop=True)
    
    colecoes_filt = df['Colecao'].unique().tolist()
    colecoes_filt.insert(0, "Todas")
    
    with col2:
        option2 = st.selectbox("Selecione a coleção desejada:", colecoes_filt)
        
    if option2 != "Todas":
        df = df[df['Colecao'] == option2]
    st.dataframe(df)
    

