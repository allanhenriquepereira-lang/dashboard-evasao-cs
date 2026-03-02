import streamlit as st
import pandas as pd

st.set_page_config(page_title="Dashboard Evasão CS - M1", layout="wide")

sheet_url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vTtVuYWi_7xz80PhQ0RhPlVi9ep7GsrsRIJwA8Pq7oaUj0U9KXCswHUCPCLd687ueppBXztA2YfX3R5/pub?output=csv"

@st.cache_data
def load_data():
    df = pd.read_csv(sheet_url)
    df.columns = df.columns.str.strip()
    return df

df = load_data()

st.title("📊 Dashboard Profissional - Alunos M1")

# FILTROS
st.sidebar.header("Filtros")

mes = st.sidebar.multiselect(
    "Mês",
    options=sorted(df["Mês"].dropna().unique()),
    default=df["Mês"].dropna().unique()
)

responsabilidade = st.sidebar.multiselect(
    "Responsabilidade",
    options=sorted(df["Responsabilidade"].dropna().unique()),
    default=df["Responsabilidade"].dropna().unique()
)

orientador = st.sidebar.multiselect(
    "Orientador",
    options=sorted(df["Orientador"].dropna().unique()),
    default=df["Orientador"].dropna().unique()
)

df_filtrado = df[
    (df["Mês"].isin(mes)) &
    (df["Responsabilidade"].isin(responsabilidade)) &
    (df["Orientador"].isin(orientador))
]

# KPIs
st.subheader("Indicadores Gerais")

col1, col2, col3 = st.columns(3)

total_contratos = df_filtrado["Contrato"].count()

if total_contratos > 0:
    taxa_resposta = (df_filtrado["Resposta"].sum() / total_contratos) * 100
    taxa_historico = (df_filtrado["Histórico"].sum() / total_contratos) * 100
else:
    taxa_resposta = 0
    taxa_historico = 0

col1.metric("Total de Contratos", total_contratos)
col2.metric("Taxa de Resposta (%)", f"{taxa_resposta:.2f}%")
col3.metric("Taxa Histórico (%)", f"{taxa_historico:.2f}%")

st.divider()

st.subheader("Contratos por Justificativa")
st.bar_chart(df_filtrado.groupby("Justificativa")["Contrato"].count())

st.subheader("Contratos por Responsabilidade")
st.bar_chart(df_filtrado.groupby("Responsabilidade")["Contrato"].count())

st.subheader("Contratos por Orientador")
st.bar_chart(df_filtrado.groupby("Orientador")["Contrato"].count())

st.subheader("Contratos por Mês")
st.bar_chart(df_filtrado.groupby("Mês")["Contrato"].count())

st.subheader("Distribuição Histórico")
st.bar_chart(df_filtrado.groupby("Histórico")["Contrato"].count())

st.subheader("Distribuição Resposta")
st.bar_chart(df_filtrado.groupby("Resposta")["Contrato"].count())
