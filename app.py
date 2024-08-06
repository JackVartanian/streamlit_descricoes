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

st.title("Acompanhamento de Produtos")
st.divider()

col1, col2, col3 = st.columns([1, 1, 1])

with col1:

    st.text("Produtos sem descrição:")
    df = pd.read_excel('arquivos/dados_prods_.xlsx')
    df = df[df['descriptionHtml'].isnull()]
    df = df[df['totalInventory'] > 0]
    df = df[['descriptionHtml', 'sku', 'title']]
    df = df.rename(columns={'descriptionHtml': 'Descrição', 'sku': 'SKU', 'title': 'Título'})
    df = df.reset_index(drop=True)
    st.dataframe(df)
    
with col2:
    
    st.text("Produtos sem Imagem:")
    df = pd.read_excel('arquivos/dados_prods_.xlsx')
    df = df[df['mediaCount.count'] == 0]
    df = df[df['totalInventory'] > 0]
    df = df[['mediaCount.count', 'sku', 'title']]
    df = df.rename(columns={'mediaCount.count': 'Imagens', 'sku': 'SKU', 'title': 'Título'})
    df = df.reset_index(drop=True)
    st.dataframe(df)
    
with col3:
    
    st.text("Produtos sem Composição:")
    df = pd.read_excel('arquivos/dados_prods_.xlsx')
    df = df[df['metafield.value'].isnull()]
    df = df[df['totalInventory'] > 0]
    df = df[['metafield.value', 'sku', 'title']]
    df = df.rename(columns={'metafield.value': 'Composição', 'sku': 'SKU', 'title': 'Título'})
    df = df.reset_index(drop=True)
    st.dataframe(df)