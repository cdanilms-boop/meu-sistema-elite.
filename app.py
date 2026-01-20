import streamlit as st
import pandas as pd
from datetime import datetime
import random

# --- CONFIGURAÇÃO DE ENGENHARIA ---
st.set_page_config(page_title="SISTEMA ELITE PRO - TESTE 1", layout="wide")

if 'banco_de_dados' not in st.session_state:
    st.session_state.banco_de_dados = []

# SIMULAÇÃO DE BANCO DE DADOS REAL (Para o Teste 1)
# Aqui colocamos alguns resultados reais históricos para testar o motor
dados_oficiais = {
    "Mega-Sena": [
        [5, 9, 32, 44, 49, 57], # Concurso 2700
        [1, 11, 19, 20, 28, 37], # Concurso 2701
        [2, 9, 11, 25, 43, 51]   # Concurso 2702
    ]
}

st.title("🚀 SISTEMA ELITE PRO - TESTE DE RESPOSTA")

# --- 1. CONFIGURAÇÃO ---
modalidade = st.sidebar.selectbox("Loteria Ativa:", ["Mega-Sena", "Lotofácil"])
regras = {
    "Mega-Sena": {"min": 150, "max": 220, "qtd": 6, "max_n": 60},
    "Lotofácil": {"min": 170, "max": 220, "qtd": 15, "max_n": 25}
}
conf = regras[modalidade]

# --- 2. GERADOR DE ELITE ---
st.subheader(f"🎲 Gerador Automático ({modalidade})")
if st.button("✨ GERAR E ANALISAR"):
    tentativas = 0
    while tentativas < 50:
        sugestao = sorted(random.sample(range(1, conf['max_n'] + 1), conf['qtd']))
        if conf['min'] <= sum(sugestao) <= conf['max']:
            st.success(f"Sugestão Gerada: **{sugestao}** | Soma: {sum(sugestao)}")
            break
        tentativas += 1

st.divider()

# --- 3. ANALISADOR E COMPARADOR (O TESTE DO MOTOR) ---
st.subheader("📝 Analisador com Busca Histórica")
col1, col2 = st.columns([2, 1])

with col1:
    entradas = []
    frentes = st.columns(6)
    for i in range(conf['qtd']):
        with frentes[i % 6]:
            num = st.number_input(f"Nº {i+1}", 1, conf['max_n'], key=f"d_{i}")
            entradas.append(num)

soma = sum(entradas)
jogo_usuario = sorted(entradas)

with col2:
    st.write(f"**Análise Técnica:**")
    # Verificação de Soma
    if conf['min'] <= soma <= conf['max']:
        st.success(f"✅ SOMA DENTRO DO PADRÃO ({soma})")
    else:
        st.warning(f"⚠️ SOMA FORA DO PADRÃO ({soma})")

    # BUSCA HISTÓRICA (O NOVO MOTOR)
    if modalidade in dados_oficiais:
        ja_saiu = False
        for resultado in dados_oficiais[modalidade]:
            if set(jogo_usuario) == set(resultado):
                ja_saiu = True
                break
        
        if ja_saiu:
            st.error("🚨 ALERTA: Este jogo JÁ FOI SORTEADO anteriormente!")
        else:
            st.info("💎 Jogo Inédito no Banco de Teste.")

# --- 4. SALVAMENTO ---
if st.button("💾 SALVAR NO BANCO DE MATURAÇÃO"):
    st.session_state.banco_de_dados.append({
        "Data": datetime.now().strftime("%d/%m %H:%M"),
        "Loteria": modalidade, 
        "Jogo": str(jogo_usuario), 
        "Soma": soma
    })
    st.toast("Salvo com sucesso!")

st.table(pd.DataFrame(st.session_state.banco_de_dados))
