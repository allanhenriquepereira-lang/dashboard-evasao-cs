import streamlit as st
import pandas as pd

st.set_page_config(page_title="Dashboard CS - Evasão", layout="wide")

# LINKS CSV
url_m1 = "https://docs.google.com/spreadsheets/d/e/2PACX-1vTtVuYWi_7xz80PhQ0RhPlVi9ep7GsrsRIJwA8Pq7oaUj0U9KXCswHUCPCLd687ueppBXztA2YfX3R5/pub?gid=1769040659&single=true&output=csv"
url_2faltas = "https://docs.google.com/spreadsheets/d/e/2PACX-1vTtVuYWi_7xz80PhQ0RhPlVi9ep7GsrsRIJwA8Pq7oaUj0U9KXCswHUCPCLd687ueppBXztA2YfX3R5/pub?gid=55844215&single=true&output=csv"
url_desistentes = "https://docs.google.com/spreadsheets/d/e/2PACX-1vTtVuYWi_7xz80PhQ0RhPlVi9ep7GsrsRIJwA8Pq7oaUj0U9KXCswHUCPCLd687ueppBXztA2YfX3R5/pub?gid=146646633&single=true&output=csv"

@st.cache_data(ttl=60)
def load_data(url):
    df = pd.read_csv(url)
    df.columns = df.columns.str.strip()
    return df

df_m1 = load_data(url_m1)
df_2faltas = load_data(url_2faltas)
df_desistentes = load_data(url_desistentes)

st.title("📊 Dashboard Completo - Controle de Evasão")

tab1, tab2, tab3 = st.tabs(["🔵 Alunos M1", "🟠 Alunos 2 Faltas", "🔴 Alunos Desistentes"])

# =======================
# ABA 1 - M1
# =======================
with tab1:
    st.subheader("Alunos M1")
    
    mes = st.selectbox("Filtrar por Mês", df_m1["Mês"].unique())
    df = df_m1[df_m1["Mês"] == mes]

    total = df["Contrato"].count()
    taxa_resposta = (df["Resposta"].sum() / total * 100) if total > 0 else 0

    col1, col2 = st.columns(2)
    col1.metric("Total Contratos", total)
    col2.metric("Taxa Resposta (%)", f"{taxa_resposta:.2f}%")

    st.bar_chart(df.groupby("Justificativa")["Contrato"].count())
    st.bar_chart(df.groupby("Orientador")["Contrato"].count())

# =======================
# ABA 2 - 2 FALTAS
# =======================
with tab2:
    st.subheader("Alunos 2 Faltas")
    
    mes2 = st.selectbox("Filtrar por Mês", df_2faltas["mês"].unique())
    df2 = df_2faltas[df_2faltas["mês"] == mes2]

    total2 = df2["Contrato"].count()
    taxa_retorno = (df2["Retorno"].sum() / total2 * 100) if total2 > 0 else 0

    col1, col2 = st.columns(2)
    col1.metric("Total Contratos", total2)
    col2.metric("Taxa Retorno (%)", f"{taxa_retorno:.2f}%")

    st.bar_chart(df2.groupby("Resposta")["Contrato"].count())

# =======================
# ABA 3 - DESISTENTES
# =======================
with tab3:
    st.subheader("Alunos Desistentes")
    
    mes3 = st.selectbox("Filtrar por Mês", df_desistentes["Mês"].unique())
    df3 = df_desistentes[df_desistentes["Mês"] == mes3]

    total3 = df3["Contrato"].count()
    taxa_hist = (df3["Historico"].sum() / total3 * 100) if total3 > 0 else 0

    col1, col2 = st.columns(2)
    col1.metric("Total Contratos", total3)
    col2.metric("Taxa Histórico (%)", f"{taxa_hist:.2f}%")

    st.bar_chart(df3.groupby("Justificativa")["Contrato"].count())
