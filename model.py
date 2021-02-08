# Se marcado como True: Exibirá no gráfico apenas os dias onde houveram diferença nos valores, das métricas de cada sistema.
PLOTAR_APENAS_OS_DIAS_COM_DIFERENCAS_NOS_VALORES_DE_CADA_SISTEMA = False


# %%
# Input dos dados.

try:
    df_total = pd.read_csv(os.path.join(TOTAL_DIR, 'Relatorio_Total.csv'))
except FileNotFoundError:
    print("Não foi possível carregar o csv 'Relatorio_Total.csv'. Por acaso ele se encontra no caminho: {}?".format(TOTAL_DIR))


# %%
# Impedindo que Sistemas considerados NÃO IDENTIFICADOS sejam exibidos no gráfico.

df_total.drop(df_total.loc[df_total['Sistema'] == "Não Identificado"].index, inplace=True)


# %%
# Criando o CSV de sistemas

# Fatiando por Data, parte do CSV de totais;
# Utilizando essas fatias para cálcular os valores obtidos por cada SISTEMA naquela data específica;
# Inserindo no sistema_df, o molde (valores resultantes obtidos por cada sistema em sua data específica).
# É importante que no CSV de totáis não possuam 2 ou mais análises do mesmo dia. Caso contrário está lógica abaixo pode gerar resultados errados nos gráficos

sistema_df = pd.DataFrame()
lista_datas = df_total.drop_duplicates(subset=['Data'])['Data'].to_numpy()

for data in lista_datas:
    # DataFrames auxiliares.
    aux_df = df_total[df_total['Data'] == data]
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
sistema_df.head(7)


# %%
# Reorganizando CSV

sistema_df = sistema_df[["MesID", "AnoID", "DataID", "Sistema", "Qtde Total Code Smells", "Qtde Total Bugs", "Qtde Total Vulnerabilidades", 'Qtde Total Linhas' ,'Qtde Total Testes', "Media Cobertura"]]
sistema_df[["MesID", "AnoID"]] = sistema_df[["MesID", "AnoID"]].apply(pd.to_numeric)
sistema_df = sistema_df.sort_values(['Sistema', 'DataID'], ascending=[True, True]) 
sistema_df.info()


# %%
# Removendo os registros que não possuem mudança nos valores.

if(PLOTAR_APENAS_OS_DIAS_COM_DIFERENCAS_NOS_VALORES_DE_CADA_SISTEMA):
    sistema_df.drop_duplicates(subset=["Sistema", "Qtde Total Code Smells", "Qtde Total Bugs", "Qtde Total Vulnerabilidades", "Media Cobertura"], inplace=True)

# %% [markdown]
# <h1>Iniciando o processo de geração dos gráficos</h1>
# <hr>

# %%
# Obtendo alguns valores auxiliares para automatizar o plot.

lista_sistemas = sistema_df['Sistema'].unique()
lista_valores = ["Qtde Total Code Smells", "Qtde Total Bugs", "Qtde Total Vulnerabilidades", "Media Cobertura"] # O nome deve de ser lista de métricas


# %%
# Definindo algumas funções auxiliares para o gráfico

def retorna_tamanho_eixo_x(qtd_datas):
    if (qtd_datas <= 5):
        return 5.5
    else:   
        return round(qtd_datas * 1.08)

def retorna_tamanho_eixo_y(qtd_datas):
    if (qtd_datas < 10):
        return 6.35
    else:   
        return round(6 * (qtd_datas / 100 + 1))

def is_plot_do_sistema_valido():
    # Não permite que sistemas que não possuem mais data de serem plotados
    if(len(sistema_df.loc[sistema_df['Sistema'] == sistema, 'DataID']) <= 1):
        return False
    else:
        return True

def retorna_mensagem_de_metricas_adicionais(sistema_df):
    try:
        linhas = sistema_df['Qtde Total Linhas'].loc[(sistema_df['Sistema'] == sistema) & (sistema_df['DataID'] == sistema_df.at[sistema_df.index[-1], 'DataID'])].values[0]
        testes = sistema_df['Qtde Total Testes'].loc[(sistema_df['Sistema'] == sistema) & (sistema_df['DataID'] == sistema_df.at[sistema_df.index[-1], 'DataID'])].values[0]
        data = sistema_df.at[sistema_df.index[-1], 'DataID']
    except:
        linhas = "Não foi possível obter a quantidade de linhas."
        testes = "Não foi possível obter a quantidade de testes. "
        data = "Não foi possível obter a última data mais recente."

    return "\nQuantidade de linhas do sistema no dia da análise: " + str(linhas) + "\nQuantidade de testes do sistema no dia da análise: " + str(testes) + "\nValores aqui exibidos são da análise do dia: " + data 


# %%
# MatPlot Testes

with PdfPages('Visualização_Relatório_Sonar' + date.today().strftime('%d_%m_%Y')  +'.pdf') as pdf:
    for sistema in lista_sistemas:
        if (is_plot_do_sistema_valido() == False):
            continue
        else:
            for index, valor in enumerate(lista_valores):
                #Obtendo os valores
                x = sistema_df.loc[sistema_df['Sistema'] == sistema, 'DataID'].values
                y = sistema_df.loc[sistema_df['Sistema'] == sistema, valor].values            
                qtd_datas = len(x)           

                # Configurando o dimensionamento do gráfico.
                plt.figure(figsize=(retorna_tamanho_eixo_x(qtd_datas), retorna_tamanho_eixo_y(qtd_datas)))
                plt.ylim(y.min() * 0.9, y.max() * 1.11)
                plt.margins(x=0.095, tight=False)
                plt.subplots_adjust(left = 0.155)

                # Configurando o Visual do gráfico.
                plt.style.use('ggplot')
                plt.grid(True, color='silver', linestyle='-.', lw=0.25)

                # Plotando os dados no gráfico
                plt.plot(x, y, linestyle='--', color='#121A5B', marker='o',linewidth=2)
                plt.xticks(rotation=40)
                plt.title('Sistema: ' + sistema)
                
                # Anotações na Linha:
                sequencia_de_valores = y
                vl_old = 0
                for vl in range(len(sequencia_de_valores)):
                    plt.annotate(str(sequencia_de_valores[vl]),
                        xy=(vl, sequencia_de_valores[vl]), xycoords='data',
                        xytext=(-7, 13.5), textcoords='offset points',
                        size=10)

                # Exibindo legenda nos gráficos
                if (qtd_datas >= 8):
                    plt.legend([valor], loc='center left', shadow=True, bbox_to_anchor=(-0.01, 1.05))
                else:
                    plt.ylabel(valor, rotation=90)
                

                # Deixando uma mensagem na primeira página de cada sistema. 
                # A mensagem é composta pelas métricas adicionais
                if(index == 1):
                    mensagem = retorna_mensagem_de_metricas_adicionais(sistema_df)
                    pdf.attach_note("Sistema: " + sistema + mensagem)
                        
                #Exporta                        
                pdf.savefig(dpi=300)
                plt.close()

    d = pdf.infodict()
    d['Author'] = 'Pedro Henrique'