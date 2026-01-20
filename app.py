import streamlit as st
import pandas as pd
from datetime import datetime
import random

# --- CONFIGURAÇÃO DO SISTEMA ---
st.set_page_config(page_title="SISTEMA ELITE PRO", layout="wide")

if 'banco_de_dados' not in st.session_state:
    st.session_state.banco_de_dados = []

st.title("🚀 SISTEMA ELITE PRO - VERSÃO 2.6")

# --- 1. CONFIGURAÇÕES NA LATERAL ---
st.sidebar.header("Painel de Controle")
modalidade = st.sidebar.selectbox(
    "Escolha a Loteria:",
    ["Mega-Sena", "Lotofácil", "Powerball (EUA)"]
)

# Regras Técnicas
regras = {
    "Mega-Sena": {"min": 150, "max": 220, "qtd": 6, "max_n": 60},
    "Lotofácil": {"min": 170, "max": 220, "qtd": 15, "max_n": 25},
    "Powerball (EUA)": {"min": 130, "max": 200, "qtd": 5, "max_n": 69}
}
conf = regras[modalidade]

# --- 2. ÁREA DE GERADOR (VOLTOU!) ---
st.subheader("🎲 Gerador de Jogos Elite")
if st.button("✨ GERAR JOGO BASEADO NA METODOLOGIA"):
    # Por enquanto gera aleatório dentro do limite, amanhã conectaremos a IA
    sugestao = sorted(random.sample(range(1, conf['max_n'] + 1), conf['qtd']))
    st.info(f"Sugestão de Elite para {modalidade}: **{sugestao}**")

st.divider()

# --- 3. AUDITORIA MANUAL (SEM O QUADRADO VERMELHO) ---
st.subheader("📝 Analisar Meus Números")
col1, col2 = st.columns([2, 1])

with col1:
    entradas = []
    frentes = st.columns(5)
    for i in range(conf['qtd']):
        with frentes[i % 5]:
            num = st.number_input(f"Nº {i+1}", 1, conf['max_n'], key=f"d_{i}")
            entradas.append(num)

soma = sum(entradas)
ordenados = sorted(entradas)

with col2:
    # Mostra a informação de forma limpa, sem o quadrado gigante
    st.write(f"**Soma Atual:** {soma}")
    if conf['min'] <= soma <= conf['max']:
        st.success(f"✅ Dentro do Padrão (Soma: {soma})")
    else:
        st.warning(f"⚠️ Atenção: Soma {soma} fora do ideal ({conf['min']}-{conf['max']})")

# --- 4. MEMÓRIA E SALVAMENTO ---
if st.button("💾 SALVAR PARA MATURAÇÃO"):
    st.session_state.banco_de_dados.append({
        "Data": datetime.now().strftime("%d/%m %H:%M"),
        "Loteria": modalidade,
        "Jogo": str(ordenados),
        "Soma": soma
    })
    st.toast("Jogo salvo com sucesso!")

st.divider()

# --- 5. BANCO DE DADOS ---
st.subheader("📂 Jogos em Maturação")
if st.session_state.banco_de_dados:
    st.table(pd.DataFrame(st.session_state.banco_de_dados))
