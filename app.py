import streamlit as st
import pandas as pd
from datetime import datetime

# CONFIGURAÇÃO DA PÁGINA
st.set_page_config(page_title="SISTEMA ELITE PRO - MULTI-LOTERIAS", layout="wide")

# --- INICIALIZAÇÃO DA MEMÓRIA ---
if 'historico_jogos' not in st.session_state:
    st.session_state['historico_jogos'] = []

st.title("🚀 SISTEMA ELITE PRO - NÍVEL 2.1")

# --- 1. SELETOR DE MODALIDADE (O que você pediu!) ---
st.markdown("### 🎯 Escolha a Loteria")
modalidade = st.selectbox(
    "Em qual base de dados vamos operar?",
    ["Mega-Sena", "Lotofácil", "+Milionária", "Powerball (EUA)"]
)

st.divider()

# --- 2. AJUSTE DINÂMICO DE REGRAS ---
if modalidade == "Mega-Sena":
    qtd_num, max_num = 6, 60
elif modalidade == "Lotofácil":
    qtd_num, max_num = 15, 25
elif modalidade == "+Milionária":
    qtd_num, max_num = 6, 50
else: # Powerball
    qtd_num, max_num = 5, 69

# --- 3. INTERFACE DE ENTRADA ---
col1, col2 = st.columns([1, 2])

with col1:
    st.info(f"📍 Configuração: {modalidade}")
    entradas = []
    for i in range(qtd_num):
        num = st.number_input(f"Dezena {i+1}", 1, max_num, key=f"num_{i}")
        entradas.append(num)

with col2:
    st.success("🤖 AUDITORIA E GERAÇÃO")
    soma_atual = sum(entradas)
    st.write(f"**Soma Atual:** {soma_atual}")
    
    c1, c2 = st.columns(2)
    with c1:
        if st.button("SALVAR JOGO"):
            st.session_state['historico_jogos'].append({
                "Loteria": modalidade, "Números": str(entradas), 
                "Soma": soma_atual, "Data": datetime.now().strftime("%d/%m/%Y %H:%M")
            })
            st.toast("Jogo salvo!")
    
    with c2:
        if st.button("GERAR JOGO ELITE 🚀"):
            # Lógica simples de geração para teste
            sugestao = sorted(pd.Series(range(1, max_num+1)).sample(qtd_num).tolist())
            st.code(f"Sugestão {modalidade}: {sugestao}")

st.divider()

# --- 4. BANCO DE DADOS DE MATURAÇÃO ---
st.write("### 📂 Jogos Salvos (Maturação)")
if st.session_state['historico_jogos']:
    df = pd.DataFrame(st.session_state['historico_jogos'])
    st.dataframe(df, use_container_width=True)
else:
    st.write("O banco de dados está vazio.")
