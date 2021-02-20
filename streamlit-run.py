import streamlit as st
import pandas as pd
import numpy as np
import os
import sys


def streamlit_interface():
    st.write('''
     ## Web Visualization of Sonarqube Data
     Testes utilizando o Framework do Streamlit ''')
    st.write('')

def retorna_mensagem_de_metricas_adicionais(sistema_df, sistema):
    try:
        linhas = sistema_df['Qtde Total Linhas'].loc[(sistema_df['Sistema'] == sistema) & (sistema_df['DataID'] == sistema_df.at[sistema_df.index[-1], 'DataID'])].values[0]
        testes = sistema_df['Qtde Total Testes'].loc[(sistema_df['Sistema'] == sistema) & (sistema_df['DataID'] == sistema_df.at[sistema_df.index[-1], 'DataID'])].values[0]
        data = sistema_df.at[sistema_df.index[-1], 'DataID']
    except:
        linhas = "Não foi possível obter a quantidade de linhas."
        testes = "Não foi possível obter a quantidade de testes. "
        data = "Não foi possível obter a última data mais recente."

    return "Quantidade de linhas do sistema no dia da análise: " + str(linhas), "Quantidade de testes do sistema no dia da análise: " + str(testes), "Valores aqui exibidos são da análise do dia: " + data 

def exibe_dados(data):

    lista_sistemas = data['Sistema'].unique()
    #lista_valores = ["Qtde Total Code Smells", "Qtde Total Bugs", "Qtde Total Vulnerabilidades", "Media Cobertura"]
    
    lista_valores = data.iloc[:, 4:].columns.tolist()
    lista_metricas_extras = ['Qtde Total Linhas', 'Qtde Total Testes']
    lista_valores.remove('Qtde Total Linhas'); lista_valores.remove('Qtde Total Testes')
    default_message = ['Selecione um item']

    with st.beta_container():
        left_column, right_column = st.beta_columns([3, 2])
        sistema = left_column.selectbox(
        label='Escolha um sistema que você deseja visualizar',
        options=default_message + lista_sistemas.tolist())

        metrica = right_column.selectbox(
        label='Escolha uma métrica que você deseja visualizar',
        options=default_message + lista_valores)
    
    
    if metrica != default_message[0] and sistema != default_message[0]:
        if st.button('Visualizar Comum'):
            st.write('### Sistema: {}'.format(sistema))
            x = data.loc[data['Sistema'] == sistema, 'DataID'].values
            y = data.loc[data['Sistema'] == sistema,  metrica].values   

            df = pd.DataFrame({
            'Data': x,
            str(metrica): y
            })

            df = df.rename(columns={'Data':'index'}).set_index('index')

            #chart_data = pd.DataFrame(dictionary = dict(zip(x,y)))
            st.line_chart(df)
            with st.beta_expander("Informações extras do Projeto"):
                msg1, msg2, msg3 = retorna_mensagem_de_metricas_adicionais(data, sistema)
                st.write(msg1)
                st.write(msg2)
                st.write(msg3)
                if st.button('Visualizar dados na tabela.'):
                    st.header("Dados do sistema: ", sistema)
                    #st.write(data.loc[data['Sistema'] == sistema, data.iloc[:, 0:].columns.tolist()])
    
def trata_dados():
    # Lendo CSV
    try:
        data_df = pd.read_csv(os.path.join("Data/Data.csv"))
    except FileNotFoundError:
        st.error("Não foi possível carregar os dados para análise")
    
    # Impedindo que Sistemas considerados NÃO IDENTIFICADOS sejam exibidos no gráfico.
    data_df.drop(data_df.loc[data_df['Sistema'] == "Não Identificado"].index, inplace=True)

    # Criando o CSV de sistemas
    sistema_df = pd.DataFrame()
    lista_datas = data_df.drop_duplicates(subset=['Data'])['Data'].to_numpy()

    for data in lista_datas:
        # DataFrames auxiliares.
        aux_df = data_df[data_df['Data'] == data]
        molde_df = pd.DataFrame()
        
        #Atribuição dos valores ao molde
        molde_df['Sistema'] = aux_df['Sistema'].unique()
        molde_df['Qtde Total Code Smells'] = aux_df.groupby(['Sistema']).sum()['Code Smells'].values
        molde_df['Qtde Total Bugs'] = aux_df.groupby(['Sistema']).sum()['Bugs'].values
        molde_df['Qtde Total Vulnerabilidades'] = aux_df.groupby(['Sistema']).sum()['Vulnerabilidades'].values
        molde_df['Qtde Total Linhas'] = aux_df[['Sistema', 'Qtde Linhas']].groupby(['Sistema']).agg(['sum']).values
        molde_df['Qtde Total Testes'] = aux_df[['Sistema', 'Qtde Testes']].groupby(['Sistema']).agg(['sum']).values
        molde_df['Media Cobertura'] = aux_df[['Sistema', 'Cobertura']].groupby(['Sistema']).agg(['mean']).values.round(2)
        molde_df['MesID'] = data[3:5]
        molde_df['AnoID'] = data[6:11]
        molde_df['DataID'] = data[0:11]
        sistema_df = sistema_df.append(molde_df, ignore_index=True)

        aux_df = None; molde_df = None

    # Reorganizando CSV

    sistema_df = sistema_df[["MesID", "AnoID", "DataID", "Sistema", "Qtde Total Code Smells", "Qtde Total Bugs", "Qtde Total Vulnerabilidades", 'Qtde Total Linhas' ,'Qtde Total Testes', "Media Cobertura"]]
    sistema_df[["MesID", "AnoID"]] = sistema_df[["MesID", "AnoID"]].apply(pd.to_numeric)
    sistema_df = sistema_df.sort_values(['Sistema', 'DataID'], ascending=[True, True]) 

    # Removendo os registros que não possuem mudança nos valores.

    #if(PLOTAR_APENAS_OS_DIAS_COM_DIFERENCAS_NOS_VALORES_DE_CADA_SISTEMA):
    #    sistema_df.drop_duplicates(subset=["Sistema", "Qtde Total Code Smells", "Qtde Total Bugs", "Qtde Total Vulnerabilidades", "Media Cobertura"], inplace=True)
    
    # Obtendo alguns valores auxiliares para automatizar o plot.
    #lista_sistemas = sistema_df['Sistema'].unique()
    #lista_valores = ["Qtde Total Code Smells", "Qtde Total Bugs", "Qtde Total Vulnerabilidades", "Media Cobertura"]

    return sistema_df

if __name__ == '__main__':
    streamlit_interface()
    exibe_dados(trata_dados())