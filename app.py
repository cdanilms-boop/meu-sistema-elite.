import streamlit as st
import pandas as pd
from datetime import datetime
import random

# --- CONFIGURAÇÃO DE ENGENHARIA ---
st.set_page_config(page_title="SISTEMA ELITE PRO - FINAL", layout="wide")

# Inicialização da Memória (Não apaga enquanto a sessão durar)
if 'banco_de_dados' not in st.session_state:
    st.session_state.banco_de_dados = []

st.title("🚀 SISTEMA ELITE PRO - VERSÃO ESTÁVEL")

# --- 1. PAINEL DE CONTROLE (LATERAL) ---
st.sidebar.header("Configuração")
modalidade = st.sidebar.selectbox("Loteria Ativa:", ["Mega-Sena", "Lotofácil", "Powerball"])

# Regras Fixas da Metodologia
regras = {
    "Mega-Sena": {"min": 150, "max": 220, "qtd": 6, "max_n": 60},
    "Lotofácil": {"min": 170, "max": 220, "qtd": 15, "max_n": 25},
    "Powerball": {"min": 130, "max": 200, "qtd": 5, "max_n": 69}
}
conf = regras[modalidade]

# --- 2. GERADOR DE JOGOS ELITE (FIXO NO TOPO) ---
st.subheader(f"🎲 Gerador Automático ({modalidade})")
if st.button("✨ GERAR JOGO PELA METODOLOGIA"):
    tentativas = 0
    while tentativas < 100:
        sugestao = sorted(random.sample(range(1, conf['max_n'] + 1), conf['qtd']))
        if conf['min'] <= sum(sugestao) <= conf['max']:
            st.success(f"Jogo Elite Gerado: **{sugestao}** | Soma: {sum(sugestao)}")
            break
        tentativas += 1

st.divider()

# --- 3. AUDITORIA MANUAL (FIXA) ---
st.subheader("📝 Analisador de Números")
col1, col2 = st.columns([2, 1])

with col1:
    entradas = []
    frentes = st.columns(6)
    for i in range(conf['qtd']):
        with frentes[i % 6]:
            num = st.number_input(f"Nº {i+1}", 1, conf['max_n'], key=f"d_{i}")
            entradas.append(num)

soma = sum(entradas)
ordenados = sorted(entradas)

with col2:
    st.write(f"**Relatório da Soma:** {soma}")
    if conf['min'] <= soma <= conf['max']:
        st.success(f"✅ JOGO APROVADO (Soma Ideal)")
        score = "100%"
    else:
        st.warning(f"⚠️ FORA DO PADRÃO ({conf['min']}-{conf['max']})")
        score = "20%"

# BOTÃO DE SALVAR (FIXO)
if st.button("💾 SALVAR NO BANCO DE DADOS DE MATURAÇÃO"):
    st.session_state.banco_de_dados.append({
        "Data": datetime.now().strftime("%d/%m %H:%M"),
        "Loteria": modalidade, 
        "Jogo": str(ordenados), 
        "Soma": soma, 
        "Força": score
    })
    st.toast("Jogo registrado na memória!")

st.divider()

# --- 4. BANCO DE DADOS (HISTÓRICO FIXO) ---
st.subheader("📂 Jogos em Maturação")
if st.session_state.banco_de_dados:
    st.table(pd.DataFrame(st.session_state.banco_de_dados))
else:
    st.info("Aguardando o primeiro jogo para salvar.")
