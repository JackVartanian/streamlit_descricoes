import datetime
import ftplib
import io
import time
from datetime import datetime
import pandas as pd
import pymssql
import requests
from numpy import where

def vendas_capta():
    url = "http://jackvartanian.net/cms/wp-content/uploads/datasets/vendas_gzip.csv"
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:66.0) Gecko/20100101 Firefox/66.0"
    }

    response = requests.get(url, headers=headers)
    df = pd.read_csv(
        io.BytesIO(response.content), sep=";", compression="gzip", low_memory=True
    )

    colunasInt = ["Qtd", "Total Liq.", "Desconto", "Custo"]
    colunasStr = ["Cod. Barras", "No.Oper"]
    df[colunasStr] = df[colunasStr].astype(str)
    df[colunasInt] = df[colunasInt].astype(int)
    df["Consultora_Nome"] = df["Consultora"].str.split(" ").str[0]
    #apagar linhas com AD e AG da coluna Grande Grupo
    descarte = ["AD", "MP", "AG", "MET", "SER"]
    df = df[~df['Grande Grupo'].isin(descarte)]
    df = df[df['Qtd'] > 0]
    
    df['Data'] = pd.to_datetime(df['Data'], format='%Y-%m-%d')
    
    
    descarte_op = ['TROCA', 'VENDA CONSIGNACAO', 'TROCA SEM BARRA']
    df = df[~df['Operacao'].isin(descarte_op)]

    return df

def ultima_fase_producao():
    url = "http://jackvartanian.net/cms/wp-content/uploads/datasets/ultima_fase_producao_gzip.csv"
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:66.0) Gecko/20100101 Firefox/66.0"
    }

    response = requests.get(url, headers=headers)
    df = pd.read_csv(
        io.BytesIO(response.content), sep=";", compression="gzip", low_memory=True
    )
    
    df['Data'] = pd.to_datetime(df['Data'], format='%Y-%m-%d')
    
    
    return df

def estoque_venda():
    url = "http://jackvartanian.net/cms/wp-content/uploads/datasets/estoque_venda_gzip.csv"
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:66.0) Gecko/20100101 Firefox/66.0"
    }

    response = requests.get(url, headers=headers)
    df = pd.read_csv(
        io.BytesIO(response.content), sep=";", compression="gzip", low_memory=True
    )
    
    return df

def estoque_barra():
    url = "http://jackvartanian.net/cms/wp-content/uploads/datasets/estoque_barra_gzip.csv"
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:66.0) Gecko/20100101 Firefox/66.0"
    }

    response = requests.get(url, headers=headers)
    df = pd.read_csv(
        io.BytesIO(response.content), sep=";", compression="gzip", low_memory=True
    )
    
    return df

def clientes():
    url = "http://jackvartanian.net/cms/wp-content/uploads/datasets/clientes_gzip.csv"
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:66.0) Gecko/20100101 Firefox/66.0"
    }
    response = requests.get(url, headers=headers)
    df = pd.read_csv(
        io.BytesIO(response.content), sep=";", compression="gzip", low_memory=False)

    dateColumns = ['Data Nascimento', 'Data Casamento']
    for col in dateColumns:
        df[col] = pd.to_datetime(df[col])

    df['Mes_Nascimento'] = df['Data Nascimento'].dt.month
    df['Dia_Nascimento'] = df['Data Nascimento'].dt.day

    df['Mes_Casamento'] = df['Data Casamento'].dt.month
    df['Dia_Casamento'] = df['Data Casamento'].dt.day

    df.fillna(0, inplace=True)

    colunasInt = ['Mes_Nascimento', 'Dia_Nascimento',
                  'Mes_Casamento', 'Dia_Casamento', 'Idade']
    df[colunasInt] = df[colunasInt].astype(int)

    df['Idade'] = where(df['Data Nascimento'] == 0, 0, df['Idade'])

    df['Regiao'] = where(df['Regiao'] == 0, 'Nao Informado', df['Regiao'])
    df['Estado'] = where(df['Estado'] == 0, 'Nao Informado', df['Estado'])
    df['Cidade'] = where(df['Cidade'] == 0, 'Nao Informado', df['Cidade'])
    df['Bairro'] = where(df['Bairro'] == 0, 'Nao Informado', df['Bairro'])

    df['Consultora'] = where(df['Consultora'] == 0, 'WEB', df['Consultora'])

    df["Cidade"] = df["Cidade"].str.normalize("NFKD").str.encode(
        "ascii", errors="ignore").str.decode("utf-8")
    df["Bairro"] = df["Bairro"].str.normalize("NFKD").str.encode(
        "ascii", errors="ignore").str.decode("utf-8")

    return df


def clientes_rfv():
    url = "http://jackvartanian.net/cms/wp-content/uploads/datasets/clientes_rfv_gzip.csv"
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:66.0) Gecko/20100101 Firefox/66.0"
    }
    response = requests.get(url, headers=headers)
    df = pd.read_csv(
        io.BytesIO(response.content), sep=";", compression="gzip", low_memory=True)

    df.drop(columns=['Proxima Compra', 'Recencia',
            'Frequencia', 'Valor'], inplace=True)
    df.fillna(0, inplace=True)

    dateColumns = ['Primeira compra', 'Ultima compra']
    df[dateColumns] = df[dateColumns].apply(pd.to_datetime, format='%Y-%m-%d')

    df['Ano_ultima_compra'] = df['Ultima compra'].dt.year
    df['Mes_ultima_compra'] = df['Ultima compra'].dt.month
    df['Anos_Marca'] = (datetime.now() - df['Primeira compra']).dt.days / 365
    df["Primeira compra"] = df["Primeira compra"].dt.strftime("%Y-%m-%d")
    df["Ultima compra"] = df["Ultima compra"].dt.strftime("%Y-%m-%d")

    intColumns = ['Total liq.', 'Qtd tickets', 'Ticket medio',
                  'Dias ultima compra', 'Media entre compras', 'Anos_Marca']
    for col in intColumns:
        df[col] = df[col].astype(int)

    return df


def produtos():
    url = "http://jackvartanian.net/cms/wp-content/uploads/datasets/produtos_gzip.csv"
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:66.0) Gecko/20100101 Firefox/66.0"
    }
    response = requests.get(url, headers=headers)
    df = pd.read_csv(
        io.BytesIO(response.content), sep=";", compression="gzip", low_memory=True
    )
    return df


def saveCSV_compression(df, file):
    start_time = time.time()
    df.to_excel('datasets/' + file + '.xlsx')
    print('Arquivo CSV Gzip gerado em %s segundos ---' %
          (round(time.time() - start_time, 2)))


def sendToFTP(filename):

    start_time = time.time()

    HOSTNAME = "ftp.jackvartanian.net"
    USERNAME = "datasets@jackvartanian.net"
    PASSWORD = "&ReI0?N0E0YMN"

    ftp_server = ftplib.FTP(HOSTNAME, USERNAME, PASSWORD)
    ftp_server.encoding = "utf-8"

    file = open('datasets/' + filename + '.xlsx', 'rb')

    ftp_server.storbinary('STOR ' + 'Fresh/' +
                          filename + '.xlsx', file, 102400)

    ftp_server.quit()

    print('Arquivo CSV enviado para o FTP em %s segundos ---' %
          (round(time.time() - start_time, 2)))
    
def limpa_telefone(telefone):
    
    telefone['Telefone'] = telefone['Telefone'].str.replace('(', '')
    telefone['Telefone'] = telefone['Telefone'].str.replace(')', '')
    telefone['Telefone'] = telefone['Telefone'].str.replace('-', '')
    telefone['Telefone'] = telefone['Telefone'].str.replace(' ', '')
    telefone['Telefone'] = telefone['Telefone'].str.replace('+', '')
    telefone['Telefone'] = telefone['Telefone'].str.replace('.', '')
    telefone['Telefone'] = telefone['Telefone'].str.replace('_', '')
    telefone['Telefone'] = telefone['Telefone'].str.replace(',', '')
    telefone['Telefone'] = telefone['Telefone'].str.replace('/', '')
    telefone['Telefone'] = telefone['Telefone'].str.replace(';', '')
    telefone['Telefone'] = telefone['Telefone'].str.replace(':', '')
    telefone['Telefone'] = telefone['Telefone'].str.replace('*', '')
    #manter apenas telefones com 9 digitos
    telefone = telefone[telefone['Telefone'].str.len() == 11]
    
    return telefone

def prepare_total_liquido():

    df = vendas_capta()
    df_contar_id_venda = df

    total_liq_cliente = df.groupby('Cod. Cliente')['Total Liq.'].sum().reset_index()
    total_liq_cliente.to_excel('csv/C_Dados_de_Venda/total_liq_cliente.xlsx', index=False)

    total_bruto_cliente = df.groupby('Cod. Cliente')['Total Brt'].sum().reset_index()
    total_bruto_cliente.to_excel('csv/C_Dados_de_Venda/total_bruto_cliente.xlsx', index=False)

    df_contar_id_venda = df_contar_id_venda[['Cod. Cliente', 'ID_Venda']]
    df_contar_id_venda = df_contar_id_venda.groupby('Cod. Cliente')['ID_Venda'].nunique().reset_index()
    df_contar_id_venda.to_excel('csv/C_Dados_de_Venda/total_vendas_cliente.xlsx', index=False)

    total_pcs_cliente = df.groupby('Cod. Cliente')['Qtd'].sum().reset_index()
    total_pcs_cliente.to_excel('csv/C_Dados_de_Venda/total_pcs_cliente.xlsx', index=False)

    # concatenar total_liq_cliente, total_pcs_cliente, total_vendas_cliente, total_produtos_cliente
    df = total_liq_cliente.merge(total_bruto_cliente, on='Cod. Cliente', how='left')
    df = df.merge(total_pcs_cliente, on='Cod. Cliente', how='left')
    df = df.merge(df_contar_id_venda, on='Cod. Cliente', how='left')
    
    df = df[df['Total Brt'] - df['Total Liq.'] > 0]

    df['Desconto_Medio'] = (df['Total Brt'] - df['Total Liq.']) / df['Total Brt'] * 100
    # deixar desconto medio com 2 casas decimais
    df['Desconto_Medio'] = df['Desconto_Medio'].round(2)
    # colocar porcentagem no campo desconto medio
    df['Desconto_Medio'] = df['Desconto_Medio'].astype(str) + '%'

    df['Ticket_Medio'] = df['Total Liq.']/df['ID_Venda']
    df['Ticket_Medio'] = df['Ticket_Medio'].round(2)
    
    #passar todas as colunas para str
    df = df.astype(str)

    df.to_excel('csv/C_Dados_de_Venda/dados_de_venda.xlsx', index=False)

    return df

def organizar_consultores(df_com_id):
    
    df_com_id['Consultora'] = df_com_id['Consultora'].replace(
        'ALINE SANTANA FERREIRA DA SILVA', 'Aline')
    df_com_id['Consultora'] = df_com_id['Consultora'].replace(
        'ANDERSON CHIAMENTI', '')
    df_com_id['Consultora'] = df_com_id['Consultora'].replace(
        'GIOVANNA DINARDI KITAGAWA', 'Giovanna')
    df_com_id['Consultora'] = df_com_id['Consultora'].replace(
        'JACK VARTANIAN', '')
    df_com_id['Consultora'] = df_com_id['Consultora'].replace(
        'JEAN JEFERSON DE MOURA', '')
    df_com_id['Consultora'] = df_com_id['Consultora'].replace(
        'JENIFFER CAROLINE LOURENCO SILVEIRA', '')
    df_com_id['Consultora'] = df_com_id['Consultora'].replace(
        'LORENA RIBEIRO RODRIGUES DE MOURA AMORIM', 'Lorena')
    df_com_id['Consultora'] = df_com_id['Consultora'].replace(
        'NICHOLAS CAVALARO DONOLA', '')
    df_com_id['Consultora'] = df_com_id['Consultora'].replace(
        'POLIANE FRANCIELE SOUZA SANTOS', 'Poliane')
    df_com_id['Consultora'] = df_com_id['Consultora'].replace(
        'ROSEANE ALVES DE MOURA', 'Roseane')
    df_com_id['Consultora'] = df_com_id['Consultora'].replace('SDR', '')
    df_com_id['Consultora'] = df_com_id['Consultora'].replace(
        'VANESSA SILVESTRE', 'Vanessa')
    df_com_id['Consultora'] = df_com_id['Consultora'].replace(
        'VENDEDOR GENERICO MATRIZ', '')
    df_com_id['Consultora'] = df_com_id['Consultora'].replace(
        'SIMARA PIRES SALOMAO', 'Simara')
    df_com_id['Consultora'] = df_com_id['Consultora'].replace(
        'THAIS VIGH DE OLIVEIRA', 'Thais')
    
    return df_com_id

def contatos_exp_fresh():
    url = "http://jackvartanian.net/cms/wp-content/uploads/datasets/Fresh/update_contatos_exp.xlsx"
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:66.0) Gecko/20100101 Firefox/66.0"
    }

    response = requests.get(url, headers=headers)
    df = pd.read_excel(
        io.BytesIO(response.content)
    )

    return df

def separa_nome_sobrenome(df):
    
    # Usar str.split para dividir a coluna 'Nome' em duas colunas: 'Nome' e 'Sobrenome'
    df[['Nome', 'Sobrenome']] = df['Nome'].str.split(n=1, expand=True)
    
    # Se 'Sobrenome' for NaN, preencha com uma string vazia
    df['Sobrenome'] = df['Sobrenome'].fillna('')
    
    return df

def conn_pymssql():
    # Parametros do banco de dados
    server = '192.168.48.9'
    database = '009JV'
    username = 'usr_pb'
    password = 'pb@18!*'

    # Criar Conexão com banco de dados
    conn = pymssql.connect(
        server, username, password, database
    )
    return conn

def sqlToPandas(sql):
    start_time = time.time()

    print('Executando SQL: ' + sql)
    conn = conn_pymssql()
    query = open(sql, 'r').read()

    print('Executando query no banco de dados')
    df = pd.read_sql(query, conn)

    print('Query executada com sucesso em %s segundos ---' %
          (round(time.time() - start_time, 2)))
    return df
    