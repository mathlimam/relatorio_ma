


import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import datetime as dt
import streamlit.components.v1 as components



#   DATAFRAMES ORIGINAIS 

REVENDEDORES = pd.read_excel('database/BASE DE DADOS COMPLETA.xlsx')
REVENDEDORES['Data'] = pd.to_datetime(REVENDEDORES['Data'], format='%d/%m/%Y')
REVENDEDORES['Data'].dt.strftime('%d/%m/%Y')

PRODUTOS = REVENDEDORES.groupby('Produto')['Quantidade'].sum().reset_index()
PRODUTOS = PRODUTOS.sort_values(by='Quantidade', ascending=False)

Produtos = PRODUTOS.head(30)

#   FIM DOS DATAFRAMES ORIGINAIS


#   SUBDATAFRAME DE FATURAMENTO DE REVENDEDORES


##faturamento_revendedores = REVENDEDORES.groupby('Cliente')['Valor Total'].sum()'''
##faturamento_revendedores.to_excel('database/faturamento_revendedores.xlsx')'''

faturamento_revendedores = pd.read_excel('database/faturamento_revendedores.xlsx')

clientes_agrupados = REVENDEDORES.groupby('Cliente')

data_ultima_compra = clientes_agrupados['Data'].max().reset_index()
valor_potencial = faturamento_revendedores['Valor Total'].mean()



data_atual = dt.datetime.now()

limite_atividade = data_atual - pd.DateOffset(months=4)


#data_ultima_compra['is_active'] = data_ultima_compra['Data'] >=limite_atividade

#data_ultima_compra.to_excel('Data ultima compra.xlsx')

#data_ultima_compra = pd.DataFrame()

data_ultima_compra = pd.read_excel('Data ultima compra.xlsx')

dataframe_combinado = pd.merge(faturamento_revendedores, data_ultima_compra, on='Cliente')
dataframe_combinado = dataframe_combinado.drop(columns=['Unnamed: 0', 'Data'])

dataframe_combinado["Potencial"] = dataframe_combinado['Valor Total'] >= valor_potencial


ativos_geral = dataframe_combinado.loc[(dataframe_combinado["is_active"] == True)]

ativos = dataframe_combinado.loc[(dataframe_combinado["is_active"] == True) & (dataframe_combinado["Potencial"] == True)]
ativos['Valor comprado'] = ativos['Valor Total'].apply(lambda x: f'R$ {x:.2f}')



inativos_geral = dataframe_combinado[dataframe_combinado["is_active"] == False]
inativos = dataframe_combinado.loc[(dataframe_combinado["is_active"] == False) & (dataframe_combinado["Potencial"] == True), ["Cliente", "Valor Total"]]
inativos['Valor comprado'] = inativos['Valor Total'].apply(lambda x: f'R$ {x:.2f}')










st.set_page_config("Estudo Distribuição", layout="centered",)

st.header("Análise de Dados: Distribuição Avatim")
st.write("")
st.markdown(f"<h5 style:'text-align:center'>Faturamento (01/2020 a 05/2024):  R$ {faturamento_revendedores['Valor Total'].sum():.2f}</h5>", unsafe_allow_html=True)
st.markdown('<br>', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)


with col1:
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.markdown(f'<h5>Quantidade de revendedores: {data_ultima_compra.shape[0]}</h3>', unsafe_allow_html=True)
    st.markdown(f'<h7>Ativos: {ativos_geral.shape[0]}</h4>', unsafe_allow_html=True)
    st.markdown(f"<h7>Inativos: {inativos_geral.shape[0]}</h4>", unsafe_allow_html=True)

with col2:
    
    labels = ['Ativos', 'Inativos']
    values=[round(ativos_geral.shape[0]/dataframe_combinado.shape[0], 2), round(inativos_geral.shape[0]/dataframe_combinado.shape[0],2)]

    fig = go.Figure(data=[go.Pie(labels=labels, values=values, pull=[0,0,0.2,0] ,hole=0.5,)])
    st.plotly_chart(fig, theme='streamlit', use_container_width=True)

with col3:
    st.write("")






    

st.markdown('<h3>Clientes expressivos</h3>', unsafe_allow_html=True)
tab1, tab2 = st.tabs(['Ativos', 'Inativos'])

with tab1:
    st.dataframe(ativos[['Cliente', 'Valor Total']].sort_values(by="Valor Total", ascending=False), height=300, use_container_width=True)

with tab2:
    st.dataframe(inativos[['Cliente', 'Valor Total']].sort_values(by="Valor Total", ascending=False), height=300, use_container_width=True)


st.markdown("<h3> Produtos mais vendidos<h3>", unsafe_allow_html=True)
figure = px.bar(Produtos.sort_values(by='Quantidade', ascending=False), x=Produtos['Produto'], y=Produtos['Quantidade'],
             labels={'x': 'Produtos', 'y': 'Quantidade de Vendas'},
             title='Top 30 Produtos Mais Vendidos')
figure.update_xaxes(tickangle=45, tickmode='linear')
st.plotly_chart(figure,use_container_width=True)


st.write("")

st.markdown("<h3> Distribuição de Faturamento no estado <h3>", unsafe_allow_html=True)
st.write("")
components.iframe("https://datawrapper.dwcdn.net/0S2QF/1/", width=700, height=700)

cidade = pd.read_excel('database/cidades.xlsx').sort_values(by="Valor Total", ascending=False)

st.dataframe(cidade[['Cidade', 'Valor Total']], use_container_width=True)
