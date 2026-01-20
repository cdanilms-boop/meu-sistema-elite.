import streamlit as st
import pandas as pd
import requests
from datetime import datetime, timedelta
import random

# ==========================================
# GAVETA 1: INTELIGÊNCIA E DADOS (O MOTOR)
# ==========================================

@st.cache_data(ttl=3600)
def obter_dados_oficiais():
    """Busca e organiza os dados sem mexer na tela"""
    try:
        url = "https://loteriascaixa-api.herokuapp.com/api/megasena"
        r = requests.get(url, timeout=10).json()
        return r
    except:
        return []

def calcular_proximo_dia():
    """Lógica pura de calendário"""
    hoje = datetime.now()
    dias_sorteio = [1, 3, 5] # Ter, Qui, Sab
    for i in range(1, 8):
        c = hoje + timedelta(days=i)
        if c.weekday() in dias_sorteio:
            semana = ["Segunda", "Terça", "Quarta", "Quinta", "Sexta", "Sábado", "Domingo"]
            return f"{semana[c.weekday()]}-feira, {c.strftime('%d/%m/%Y')}"
    return "A definir"

# ==========================================
# GAVETA 2: VISUAL E INTERFACE (A LATARIA)
# ==========================================

st.set_page_config(page_title="ELITE PRO V5.2", layout="wide")

# Carregamento Inicial
dados_brutos = obter_dados_oficiais()
if dados_brutos:
    ultimo_j = dados_brutos[0]
    data_prox = calcular_proximo_dia()

# --- SIDEBAR (COMANDOS) ---
with st.sidebar:
    st.title("🛡️ PAINEL DE CONTROLE")
    
    if dados_brutos:
        with st.container(border=True):
            st.markdown(f"**CONCURSO {ultimo_j['concurso']}**")
            st.subheader(" ".join([f"[{n}]" for n in ultimo_j['dezenas']]))
            if ultimo_j['acumulou']:
                st.warning(f"💰 ACUMULADO: R$ {ultimo_j['valorEstimadoProximoConcurso']:,.2f}")
            st.info(f"📅 Próximo: {data_prox}")

    st.divider()
    # Banco de Maturação na lateral para limpar o centro
    st.header("📂 MATURAÇÃO")
    if 'banco' not in st.session_state: st.session_state.banco = []
    if st.session_state.banco:
        st.table(pd.DataFrame(st.session_state.banco))
    
    if st.button("💾 SALVAR JOGO ATUAL", type="primary", use_container_width=True):
        jogo_v = sorted([st.session_state[f"v_{i}"] for i in range(6)])
        st.session_state.banco.append({"Jogo": str(jogo_v), "Soma": sum(jogo_v)})
        st.rerun()

# --- CENTRO (EXECUÇÃO) ---
st.title("🔎 SCANNER DE AUDITORIA")

# Entrada de Dados
cols = st.columns(6)
for i in range(6):
    with cols[i]:
        st.number_input(f"Nº {i+1}", 1, 60, key=f"v_{i}")

meu_jogo = sorted([st.session_state[f"v_{i}"] for i in range(6)])

# Execução do Scanner
if st.button("🚀 EXECUTAR SCANNER", use_container_width=True):
    st.divider()
    soma = sum(meu_jogo)
    
    # Validação de Harvard
    if 150 <= soma <= 220:
        st.success(f"✅ CRITÉRIO SOMA: {soma} (DENTRO DA ZONA DE OURO)")
    else:
        st.warning(f"⚠️ CRITÉRIO SOMA: {soma} (FORA DO PADRÃO)")
    
    # Verificação de Ineditismo Global
    if dados_brutos:
        conflitos = [j for j in dados_brutos if len(set(meu_jogo).intersection(set(map(int, j['dezenas'])))) >= 4]
        if not conflitos:
            st.balloons()
            st.info("💎 EXCLUSIVO: Este jogo nunca teve 4 ou mais acertos na história.")
        else:
            st.error(f"🚨 CONFLITO: Encontrado em {len(conflitos)} concursos passados.")
