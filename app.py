import streamlit as st
import pandas as pd
import numpy as np
import requests
import io
# importar função de uma pasta no nível acima
import sys
import os
import openpyxl
import f_funcoes as fun

st.set_page_config(
    page_title="Acompanhameto de Produtos",
    page_icon="💎",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.header("Acompanhamento de Produtos Shopify", divider="blue")

df = pd.read_csv('arquivos/dados_prods_.csv', sep=';', encoding='utf-8')
df_prod = fun.produtos()

df_prod = df_prod[['Cod. Prod.', 'Desc. Produto']]

col4, col5, col6 = st.columns([1, 1, 1])

df = df[df['totalInventory'] > 0]
df_total = df.shape[0]
df_descricao = df[df['descriptionHtml'].isnull()]
df_imagem = df[df['mediaCount.count'] == 0]
df_composicao = df[df['metafield.value'].isnull()]
df_descricao_count = df_descricao.shape[0]
df_imagem_count = df_imagem.shape[0]
df_composicao_count = df_composicao.shape[0]

rel_desc = df_descricao_count / df_total * 100 * -1
rel_desc = round(rel_desc, 2)
rel_desc = str(rel_desc) + "%"

rel_imag = df_imagem_count / df_total * 100 * -1
rel_imag = round(rel_imag, 2)
rel_imag = str(rel_imag) + "%"

rel_comp = df_composicao_count / df_total * 100 * -1
rel_comp = round(rel_comp, 2)
rel_comp = str(rel_comp) + "%"

col4, col5, col6 = st.columns([1, 1, 1])
with col4:
    container = st.container()
    with container:
        st.metric("Quantidade de produtos sem descrição:", df_descricao_count, rel_desc)

with col5:
    container = st.container()
    with container:
        st.metric("Quantidade de produtos sem imagem:", df_imagem_count, rel_imag)
with col6:
    container = st.container()
    with container:
        st.metric("Quantidade de produtos sem composição:", df_composicao_count, rel_comp)

container = st.container()
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
    "BOLD"
]

with col1:
    option = st.selectbox("Selecione a opção desejada:", ["Produtos sem descrição", "Produtos sem imagem", "Produtos sem composição", "Todos"])

if option == "Produtos sem descrição":
    st.subheader("Produtos sem descrição:")

    df_filtered = df_descricao.copy()
    qtd_produtos = df_filtered.shape[0]
    df_filtered = df_filtered[colunas_comuns]
    df_filtered = pd.merge(df_filtered, df_prod, left_on='sku', right_on='Cod. Prod.', how='left')
    #passar a coluna Desc. Produto para a terceira posição
    cols = df_filtered.columns.tolist()
    cols = cols[:2] + cols[-1:] + cols[2:-1]
    df_filtered = df_filtered[cols]
    df_filtered['Novo Título'] = ""
    df_filtered['Desc. Mkt'] = ""
    df_filtered = df_filtered.rename(columns={'sku': 'SKU', 'title': 'Título no Shopify'})
    df_filtered = df_filtered.reset_index(drop=True)

    colecoes_filt = df_filtered['Colecao'].unique().tolist()
    colecoes_filt.insert(0, "Todas")

    with col2:
        option2 = st.selectbox("Selecione a coleção desejada:", colecoes_filt)

    if option2 != "Todas":
        df_filtered = df_filtered[df_filtered['Colecao'] == option2]
    st.dataframe(df_filtered)

    # Export to Excel
    excel_file = io.BytesIO()
    with pd.ExcelWriter(excel_file, engine='openpyxl') as writer:
        df_filtered.to_excel(writer, index=False)
    excel_file.seek(0)
    st.download_button(
        label="Download dados em Excel",
        data=excel_file,
        file_name='produtos_sem_descricao.xlsx',
        mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )

elif option == "Produtos sem imagem":
    st.subheader("Produtos sem Imagem:")

    df_filtered = df_imagem.copy()
    qtd_imagens = df_filtered.shape[0]
    df_filtered = df_filtered[colunas_comuns]
    df_filtered = df_filtered.rename(columns={'mediaCount.count': 'Imagens', 'sku': 'SKU', 'title': 'Título no Shopify'})
    df_filtered = df_filtered.reset_index(drop=True)

    colecoes_filt = df_filtered['Colecao'].unique().tolist()
    colecoes_filt.insert(0, "Todas")

    with col2:
        option2 = st.selectbox("Selecione a coleção desejada:", colecoes_filt)

    if option2 != "Todas":
        df_filtered = df_filtered[df_filtered['Colecao'] == option2]
    st.dataframe(df_filtered)

    # Export to Excel
    excel_file = io.BytesIO()
    with pd.ExcelWriter(excel_file, engine='openpyxl') as writer:
        df_filtered.to_excel(writer, index=False)
    excel_file.seek(0)
    st.download_button(
        label="Download dados em Excel",
        data=excel_file,
        file_name='produtos_sem_imagem.xlsx',
        mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )

elif option == "Produtos sem composição":
    st.subheader("Produtos sem Composição:")

    df_filtered = df_composicao.copy()
    qtd_composicao = df_filtered.shape[0]
    df_filtered = df_filtered[colunas_comuns]
    df_filtered = df_filtered.rename(columns={'metafield.value': 'Composição', 'sku': 'SKU', 'title': 'Título no Shopify'})
    df_filtered = df_filtered.reset_index(drop=True)

    colecoes_filt = df_filtered['Colecao'].unique().tolist()
    colecoes_filt.insert(0, "Todas")

    with col2:
        option2 = st.selectbox("Selecione a coleção desejada:", colecoes_filt)

    if option2 != "Todas":
        df_filtered = df_filtered[df_filtered['Colecao'] == option2]
    st.dataframe(df_filtered)

    # Export to Excel
    excel_file = io.BytesIO()
    with pd.ExcelWriter(excel_file, engine='openpyxl') as writer:
        df_filtered.to_excel(writer, index=False)
    excel_file.seek(0)
    st.download_button(
        label="Download dados em Excel",
        data=excel_file,
        file_name='produtos_sem_composicao.xlsx',
        mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    
elif option == "Todos":
    st.subheader("Todos os produtos:")

    df_filtered = df.copy()
    df_filtered = df_filtered[colunas_comuns]
    df_filtered = pd.merge(df_filtered, df_prod, left_on='sku', right_on='Cod. Prod.', how='left')
    #passar a coluna Desc. Produto para a terceira posição
    cols = df_filtered.columns.tolist()
    cols = cols[:2] + cols[-1:] + cols[2:-1]
    df_filtered = df_filtered[cols]
    df_filtered['Novo Título'] = ""
    df_filtered['Desc. Mkt'] = ""
    df_filtered = df_filtered.rename(columns={'sku': 'SKU', 'title': 'Título no Shopify'})
    df_filtered = df_filtered.reset_index(drop=True)

    colecoes_filt = df_filtered['Colecao'].unique().tolist()
    colecoes_filt.insert(0, "Todas")

    with col2:
        option2 = st.selectbox("Selecione a coleção desejada:", colecoes_filt)

    if option2 != "Todas":
        df_filtered = df_filtered[df_filtered['Colecao'] == option2]
    st.dataframe(df_filtered)

    # Export to Excel
    excel_file = io.BytesIO()
    with pd.ExcelWriter(excel_file, engine='openpyxl') as writer:
        df_filtered.to_excel(writer, index=False)
    excel_file.seek(0)
    st.download_button(
        label="Download dados em Excel",
        data=excel_file,
        file_name='todos_produtos.xlsx',
        mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
