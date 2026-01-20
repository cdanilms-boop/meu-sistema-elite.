import streamlit as st
import pandas as pd
from datetime import datetime
import random

st.set_page_config(page_title="SISTEMA ELITE PRO - V3.9", layout="wide")

# Memória do Sistema
if 'banco_de_dados' not in st.session_state:
    st.session_state.banco_de_dados = []

# --- MOTOR DE INTELIGÊNCIA ---
DEZENAS_ELITE = [10, 5, 53, 4, 33, 23, 54, 42, 37, 27, 30, 44, 17, 11, 29]

@st.cache_data
def carregar_historico():
    return [
        {"concurso": "53", "data": "20/03/1997", "nums": {2, 3, 14, 17, 45, 50}},
        {"concurso": "2700", "data": "15/01/2024", "nums": {2, 10, 17, 22, 30, 58}},
        {"concurso": "2750", "data": "18/07/2024", "nums": {1, 5, 14, 25, 33, 48}}
    ]

# Captura de dados global para acesso pela sidebar
c_min, c_max, c_qtd, c_n = 150, 220, 6, 60

# --- LÓGICA DE ENTRADA CENTRAL ---
st.title("🔎 SCANNER PROFISSIONAL")
st.markdown("### 1. Digite seu Volante")

cols = st.columns(6)
entradas = []
for i in range(c_qtd):
    with cols[i % 6]:
        num = st.number_input(f"Nº {i+1}", 1, c_n, key=f"v_{i}")
        entradas.append(num)

meu_jogo = sorted(list(set(entradas)))
soma_u = sum(meu_jogo)
pares = len([n for n in meu_jogo if n % 2 == 0])
impares = 6 - pares

# Botão de Execução Central
if st.button("🚀 EXECUTAR DIAGNÓSTICO", use_container_width=True):
    historico = carregar_historico()
    st.divider()
    
    col_a, col_b = st.columns(2)
    with col_a:
        if c_min <= soma_u <= c_max: st.success(f"✅ SOMA: {soma_u} (IDEAL)")
        else: st.warning(f"⚠️ SOMA: {soma_u} (FORA DO PADRÃO)")
    with col_b:
        if pares in [2, 3, 4]: st.success(f"⚖️ PARIDADE: {pares}P/{impares}Í (OK)")
        else: st.error(f"❌ PARIDADE: {pares}P/{impares}Í (RISCO)")

    conflito = False
    for h in historico:
        iguais = set(meu_jogo).intersection(h['nums'])
        if len(iguais) >= 4:
            conflito = True
            st.error(f"🚨 CONFLITO NO CONCURSO {h['concurso']} ({h['data']})")
            st.write(f"Repetidos: {sorted(list(iguais))}")
            
            # Recalibragem
            base = sorted(list(iguais))[:2]
            while True:
                sobra = random.sample([n for n in DEZENAS_ELITE if n not in meu_jogo], 4)
                final = sorted(base + sobra)
                if c_min <= sum(final) <= c_max:
                    st.info(f"💡 **SUGESTÃO DE RECALIBRAGEM:**")
                    st.success(f"✅ NOVO JOGO VALIDADO: {final} (Soma: {sum(final)})")
                    break
    
    if not conflito: st.info("💎 JOGO INÉDITO DETECTADO.")

# --- BARRA LATERAL (AÇÕES E BANCO) ---
with st.sidebar:
    st.title("🛡️ PAINEL DE CONTROLE")
    
    st.header("⚙️ Configurações")
    st.selectbox("Modalidade:", ["Mega-Sena"])
    
    st.divider()
    
    # GERADOR NA LATERAL
    if st.button("✨ GERAR SUGESTÃO RÁPIDA"):
        base = random.sample(DEZENAS_ELITE, 3) + random.sample(range(1, 61), 3)
        sug_final = sorted(list(set(base)))[:6]
        st.code(f"{sug_final}")

    st.divider()

    # SALVAMENTO NA LATERAL (Sua solicitação)
    st.header("💾 Ação Final")
    if st.button("CONFIRMAR E SALVAR JOGO", type="primary", use_container_width=True):
        if len(meu_jogo) < 6:
            st.error("Insira 6 números primeiro.")
        else:
            st.session_state.banco_de_dados.append({
                "Jogo": str(meu_jogo), "Soma": soma_u
            })
            st.toast("Jogo salvo na lista abaixo!")
            st.rerun()

    st.divider()
    
    # BANCO NA LATERAL
    st.header("📂 MATURAÇÃO")
    if st.session_state.banco_de_dados:
        df_mat = pd.DataFrame(st.session_state.banco_de_dados)
        st.dataframe(df_mat, hide_index=True)
        if st.button("🗑️ Limpar Tudo"):
            st.session_state.banco_de_dados = []
            st.rerun()
