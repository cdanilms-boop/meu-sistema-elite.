import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime

# CONFIGURAÇÃO DA PÁGINA
st.set_page_config(page_title="SISTEMA ELITE PRO - NÍVEL 2", layout="wide")

# --- MEMÓRIA DO SISTEMA (BANCO DE DADOS SIMULADO) ---
# Aqui o sistema começa a guardar o que aconteceu no passado
if 'historico_jogos' not in st.session_state:
    st.session_state['historico_jogos'] = []

# TÍTULO
st.title("🚀 SISTEMA ELITE PRO - NÍVEL 2")
st.subheader("Motor de Memória e Auditoria Ativa")

# --- COLUNAS PRINCIPAIS ---
col1, col2, col3 = st.columns(3)

with col1:
    st.info("📊 ANÁLISE ESTATÍSTICA")
    num1 = st.number_input("Dezena 1", 1, 60, 1)
    num2 = st.number_input("Dezena 2", 1, 60, 10)
    num3 = st.number_input("Dezena 3", 1, 60, 20)
    num4 = st.number_input("Dezena 4", 1, 60, 30)
    num5 = st.number_input("Dezena 5", 1, 60, 40)
    num6 = st.number_input("Dezena 6", 1, 60, 50)
    
    jogo_usuario = [num1, num2, num3, num4, num5, num6]

with col2:
    st.success("🤖 MOTOR HARVARD (AUDITORIA)")
    soma = sum(jogo_usuario)
    st.write(f"**Soma das Dezenas:** {soma}")
    
    # Filtro de Soma
    if 150 <= soma <= 220:
        st.write("✅ Soma: IDEAL")
    else:
        st.write("⚠️ Soma: FORA DO PADRÃO")

    if st.button("ANALISAR JOGO"):
        st.write(f"Analisando jogo: {jogo_usuario}...")
        # Lógica de Auditoria Nível 1 + Memória
        st.session_state['historico_jogos'].append({"jogo": jogo_usuario, "data": datetime.now(), "status": "Analisado"})
        st.balloons()

with col3:
    st.warning("💾 MEMÓRIA E SALVAMENTO")
    if st.button("SALVAR PARA MATURAÇÃO"):
        # Aqui o jogo fica guardado no sistema
        st.session_state['historico_jogos'].append({"jogo": jogo_usuario, "data": datetime.now(), "status": "Em Maturação"})
        st.write("Jogo salvo na memória do sistema!")

st.divider()

# --- ÁREA DE HISTÓRICO (O que o sistema já sabe) ---
st.write("### 📂 Jogos na Memória (Aguardando Sorteio)")
if st.session_state['historico_jogos']:
    df = pd.DataFrame(st.session_state['historico_jogos'])
    st.table(df)
else:
    st.write("Nenhum jogo salvo ainda.")
