# Bibliotecas importadas
from statistics import linear_regression
import streamlit as st
from backend import adicionar_transacao, gerar_bkp_e_limpar, obter_saldo
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
from sklearn.linear_model import LinearRegression
import numpy as np

# Titulo do site
st.sidebar.markdown("<h1 style='text-align: left;'>💸 Análise Financeira</h1>", unsafe_allow_html=True)

# ======== BLOCO DE FILTROS ========

# Carrega os dados para os filtros
df = pd.read_csv('dados_financeiros.csv')
df['Data'] = pd.to_datetime(df['Data'])

# Cria as Colunas para ps Filtros
col1, col2, col3, col4 = st.columns(4)

# Filtro por tipo
tipo_selecionado = col2.selectbox('Tipo de Transação', ['Todos', 'Entrada', 'Saída'])

# Filtro por banco
banco_selecionado = col1.selectbox('Filtrar por Banco', ['Todos'] + sorted(df['Banco'].unique().tolist()))

# Filtro por mês
meses = df['Data'].dt.strftime('%m-%y').unique()
mes_selecionado = col3.selectbox('Mês',['Todos'] + sorted(meses))

#Filtros
# Filtros aplicados ao DATAFRAME
df_filtrado = df.copy()
if banco_selecionado != 'Todos':
    df_filtrado = df_filtrado[df_filtrado["Banco"] == banco_selecionado]

if tipo_selecionado != "Todos":
    df_filtrado = df_filtrado[df_filtrado["Tipo"] == tipo_selecionado]

if mes_selecionado != "Todos":
    df_filtrado = df_filtrado[df_filtrado["Data"].dt.strftime('%m-%y') == mes_selecionado]

# ======== BLOCO DE INSERÇÃO DE DADOS ========

# seção de inserção de dados
st.sidebar.header('Inserção de Dados')

# Campos de entrada
data_transacao = st.sidebar.date_input('Data de transação', value=datetime.today())

tipo = st.sidebar.selectbox('Tipo de Transação', ['Entrada', 'Saída'])
banco = st.sidebar.selectbox('Banco', ['Nubank', 'Banco do Brasil', 'Caixa Economica'])

if tipo == 'Entrada':
    categoria = st.sidebar.selectbox('Categoria', ['Salário', 'Vendas', 'Dividendos/Investimentos'])
else:
    categoria = st.sidebar.selectbox('Categoria', ['Apartamento',
                                                   'Casa',
                                                   'Celular',
                                                   'Lanches/Comida',
                                                   'Super. Essencial',
                                                   'Super. Diferente',
                                                   'Impressão 3D',
                                                   'Combustivel/Manut.',
                                                   'Presentes',
                                                   'Lazer',
                                                   'Roupas/Calçados',
                                                   'Cuidados Pessoais',
                                                   'Assinaturas',
                                                   'SemParar',
                                                   'Cartão de Credito'
    ])

descricao = st.sidebar.text_input('Descrição')
valor = st.sidebar.number_input('valor', step=0.01)

#Botão para adicionar a transação
if st.sidebar.button('💲Adicionar Transação'):
    adicionar_transacao(tipo, categoria, banco, descricao, valor, data_transacao)
    st.sidebar.success('Transação Adicionada com SUCESSO!!')

#Botão para limpar todos os dados do arquivo CSV!!!! Perigoso
if st.sidebar.button('🔄 Gerar Backup e Limpar Dados!!!!'):
    gerar_bkp_e_limpar()
    st.sidebar.success('Backup criado e dados limpos com sucesso!')

# # ======== BLOCO DE GRÁFICOS / CARTÕES COM VALORES ========

# cartões com os saldos
#calcula os saldos usando sua função
saldo_nubank = obter_saldo('Nubank', df)
saldo_bb = obter_saldo('Banco do Brasil', df)
saldo_caixa = obter_saldo('Caixa Economica',df)

# formatar a cor
def formatar_saldo(valor):
    cor = 'green' if valor >= 0 else 'red'
    return f"<h3 style='color:{cor};'>R$: {valor:.2f}</h3>"

# Exibir os cartões
cart1, cart2, cart3 = st.columns(3)

with cart1:
    st.markdown('##### 💳 Nubank')
    st.markdown(formatar_saldo(saldo_nubank), unsafe_allow_html=True)

with cart2:
    st.markdown('##### 🏦 Banco do Brasil')
    st.markdown(formatar_saldo(saldo_bb), unsafe_allow_html=True)

with cart3:
    st.markdown('##### 💰 Caixa Econômica')
    st.markdown(formatar_saldo(saldo_caixa), unsafe_allow_html=True)


# Criar a coluna Ano/Mês
df_filtrado['AnoMes'] = df_filtrado['Data'].dt.to_period('M').astype(str)

# agrupa entradas e saídas por mês
entradas = df_filtrado[df_filtrado['Tipo'] == 'Entrada'].groupby('AnoMes')['Valor'].sum()
saidas = df_filtrado[df_filtrado['Tipo'] == 'Saída'].groupby('AnoMes')['Valor'].sum().abs()

# Garante que todos os meses estejam presentes
todos_meses = sorted(set(entradas.index).union(set(saidas.index)))
entradas = entradas.reindex(todos_meses, fill_value=0)
saidas = saidas.reindex(todos_meses, fill_value=0)

# Criação do grafico de linhas com as saidas por mes/ano
fig1 = go.Figure()
fig1.add_trace(go.Scatter(
    x=todos_meses,
    y=entradas,
    mode='lines+markers',
    name='Entradas',
    line=dict(color='green', width=2)
))
fig1.add_trace(go.Scatter(
    x=todos_meses,
    y=saidas,
    mode='lines+markers',
    name='Saídas',
    line=dict(color='red', width=2)
))
fig1.update_layout(
    title='📈 Entradas vs Saídas por Mês',
    xaxis_title='Ano/Mês',
    yaxis_title='Valor (R$)',
    legend_title='Tipo de Transação',
    hovermode='x unified',
    height=400,
)

# Grafico de rosca mostrando as saidas por categorias
df_saida = df[df['Tipo'] == 'Saída']
if banco_selecionado != 'Todos':
      df_saida = df_saida[df_saida['Banco'] == banco_selecionado]
if mes_selecionado != 'Todos':
      df_saida = df_saida[df_saida['Data'].dt.strftime('%m-%y') == mes_selecionado]
df_saida = df_saida[df_saida['Tipo'] == 'Saída']

gastos_por_categoria = df_saida.groupby('Categoria')['Valor'].sum().abs().reset_index()

fig2 = px.pie(
    gastos_por_categoria,
    names='Categoria',
    values='Valor',
    title='🍩 Distribuição de Saídas por Categoria',
    hole=0.5,
)

# Grafico de barras por bancos (entrada e saida Separada)
gastos_por_banco = df_filtrado.groupby(['Banco', 'Tipo'])['Valor'].sum().reset_index()
fig3 = px.bar(
    gastos_por_banco,
    x='Banco',
    y='Valor',
    color='Tipo',
    barmode='group',
    title='🏦 Entradas e Saídas por Banco',
    labels={'Valor': 'Valor (R$)', 'Banco': 'Instituição'}
)

# Grafico de área acumulada (evolução de Saldo)
# Ordenação por data
df_filtrado = df_filtrado.sort_values('Data')
#converte entradas em positivo e saidas em negativo
df_filtrado['Valor_Ajustado'] = df_filtrado.apply(
    lambda row: row['Valor'] if row['Tipo'] =='Entrada' else -row['Valor'], axis=1
)
#Calcula o saldo acumulado
df_filtrado['Saldo_Acumulado'] = df_filtrado['Valor_Ajustado'].cumsum()

# Criar o grafico de área
fig4 = go.Figure()
fig4.add_trace(go.Scatter(
    x=df_filtrado['Data'],
    y=df_filtrado['Saldo_Acumulado'],
    mode='lines',
    fill='tozeroy',
    line=dict(color='blue'),
    name='Saldo Acumulado'
))

fig4.update_layout(
    title='📈 Evolução do Saldo Acumulado',
    xaxis_title='Data',
    yaxis_title='Saldo (R$)',
    hovermode='x unified',
    height=400
)

# Heatmap de gastos por dia da semana
# Filtra apenas saídas (gastos)
df_gastos = df_filtrado[df_filtrado['Tipo'] == 'Saída']

# Cria coluna com nome do dia da semana em inglês
df_gastos['DiaSemanaEN'] = df_gastos['Data'].dt.day_name()

# Traduz os dias para português
traducao_dias = {
    'Monday': 'Segunda',
    'Tuesday': 'Terça',
    'Wednesday': 'Quarta',
    'Thursday': 'Quinta',
    'Friday': 'Sexta',
    'Saturday': 'Sabado',
    'Sunday': 'Domingo'
}
df_gastos['DiaSemana'] = df_gastos['DiaSemanaEN'].map(traducao_dias)

# Agrupa os gastos por dia da semana
gastos_semana = df_gastos.groupby('DiaSemana')['Valor'].sum().reset_index()

# Garante a ordem dos dias
ordem_dias_pt = ['Segunda', 'Terça', 'Quarta', 'Quinta', 'Sexta', 'Sabado', 'Domingo']
gastos_semana = gastos_semana.set_index('DiaSemana').reindex(ordem_dias_pt).fillna(0)

# Cria o heatmap
fig6 = go.Figure(data=go.Heatmap(
    z=[gastos_semana['Valor'].values],
    x=gastos_semana.index,
    y=['Gastos'],
    colorscale='Reds',
    showscale=True,
    hovertemplate='Dia: %{x}<br>Valor: R$ %{z:.2f}<extra></extra>'
))

fig6.update_layout(
    title='🔥 Gastos por Dia da Semana',
    xaxis_title='Dia da Semana',
    yaxis_title='',
    height=400
)

# # ======== ORGANIZANDO OS GRAFICOS NO STREAMLIT ========
st.plotly_chart(fig1, use_container_width=True, key='grafico_linhas')

col_graf1, col_graf2 = st.columns(2)

with col_graf1:
    st.plotly_chart(fig2, use_container_width=True, key='grafico_rosca')

with col_graf2:
    st.plotly_chart(fig3, use_container_width=True, key='grafico_barras_banco')

col_graf3, col_graf4 = st.columns(2)

with col_graf3:
    st.plotly_chart(fig4, use_container_width=True, key='grafico_area_saldo')

with col_graf4:
    st.plotly_chart(fig6, use_container_width=True, key='grafico_heatmap_semana')


#matriz dos dados
st.markdown('### 📋 Dados Na Integra')
st.dataframe(df_filtrado, use_container_width=True)