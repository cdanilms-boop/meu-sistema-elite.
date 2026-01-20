import streamlit as st
import pandas as pd
from datetime import datetime
import random

st.set_page_config(page_title="SISTEMA ELITE PRO - V3.7", layout="wide")

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

# --- BARRA LATERAL UNIFICADA ---
with st.sidebar:
    st.title("🛡️ CONTROLE ELITE")
    
    # 1. Configurações
    st.header("⚙️ Ajustes")
    modalidade = st.selectbox("Loteria Ativa:", ["Mega-Sena"])
    c_min, c_max, c_qtd, c_n = 150, 220, 6, 60
    
    st.divider()
    
    # 2. Gerador na Lateral
    st.header("✨ Sugestão")
    if st.button("GERAR JOGO DE ELITE"):
        for _ in range(1000):
            base = random.sample(DEZENAS_ELITE, 3) + random.sample(range(1, 61), 3)
            sugestao = sorted(list(set(base)))
            if len(sugestao) == 6:
                p_teste = len([x for x in sugestao if x % 2 == 0])
                if c_min <= sum(sugestao) <= c_max and p_teste in [2,3,4]:
                    st.success(f"JOGO: {sugestao}")
                    st.caption(f"Soma: {sum(sugestao)} | {p_teste}P/{(6-p_teste)}Í")
                    break
    
    st.divider()
    
    # 3. Banco de Maturação
    st.header("📂 MATURAÇÃO")
    if st.session_state.banco_de_dados:
        df_maturacao = pd.DataFrame(st.session_state.banco_de_dados)
        st.dataframe(df_maturacao[['Jogo', 'Soma']], hide_index=True)
        if st.button("🗑️ Limpar Banco"):
            st.session_state.banco_de_dados = []
            st.rerun()
    else:
        st.info("Banco vazio.")

# --- ÁREA CENTRAL (LIMPA) ---
st.title("🔎 SCANNER DE AUDITORIA")
st.markdown("Insira as dezenas do seu volante para verificar conformidade estatística e histórico.")

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

if st.button("🔍 EXECUTAR SCANNER PROFISSIONAL", use_container_width=True):
    historico = carregar_historico()
    st.divider()
    
    col_a, col_b = st.columns(2)
    with col_a:
        if c_min <= soma_u <= c_max: st.success(f"✅ SOMA: {soma_u} (DENTRO)")
        else: st.warning(f"⚠️ SOMA: {soma_u} (FORA)")
    with col_b:
        if pares in [2, 3, 4]: st.success(f"⚖️ PARIDADE: {pares}P/{impares}Í (OK)")
        else: st.error(f"❌ PARIDADE: {pares}P/{impares}Í (RISCO)")

    conflito = False
    for h in historico:
        iguais = set(meu_jogo).intersection(h['nums'])
        if len(iguais) >= 4:
            conflito = True
            st.error(f"🚨 CONCURSO {h['concurso']} ({h['data']}) detectado!")
            st.write(f"Dezenas repetidas: {sorted(list(iguais))}")
            
            # Recalibragem
            base = sorted(list(iguais))[:2]
            tentativas = 0
            while tentativas < 1000:
                candidatos = [n for n in DEZENAS_ELITE if n not in meu_jogo]
                sobra = random.sample(candidatos, 4)
                final = sorted(base + sobra)
                if c_min <= sum(final) <= c_max:
                    st.info(f"💡 **SUGESTÃO DE TROCA METÓDICA:**")
                    st.success(f"✅ NOVO JOGO: {final} (Soma: {sum(final)})")
                    break
                tentativas += 1

    if not conflito: st.info("💎 JOGO INÉDITO NO BANCO DE DADOS.")

st.divider()
if st.button("💾 CONFIRMAR E SALVAR NO BANCO", use_container_width=True):
    if len(meu_jogo) < 6:
        st.error("Preencha as 6 dezenas.")
    else:
        st.session_state.banco_de_dados.append({
            "Jogo": str(meu_jogo), "Soma": soma_u, "Paridade": f"{pares}P/{impares}Í"
        })
        st.toast("Salvo com sucesso!")
        st.rerun()
