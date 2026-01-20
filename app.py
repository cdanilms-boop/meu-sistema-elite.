import streamlit as st
import pandas as pd
from datetime import datetime
import random

st.set_page_config(page_title="SISTEMA ELITE PRO - V3.8", layout="wide")

# Inicialização da Memória
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

# --- BARRA LATERAL (CENTRAL DE COMANDOS) ---
with st.sidebar:
    st.title("🛡️ PAINEL ELITE")
    
    # 1. Configurações
    st.header("⚙️ Configurações")
    modalidade = st.selectbox("Loteria Ativa:", ["Mega-Sena"])
    c_min, c_max, c_qtd, c_n = 150, 220, 6, 60
    
    st.divider()
    
    # 2. Gerador
    st.header("✨ Gerador")
    if st.button("GERAR NOVA SUGESTÃO"):
        for _ in range(1000):
            base = random.sample(DEZENAS_ELITE, 3) + random.sample(range(1, 61), 3)
            sugestao = sorted(list(set(base)))
            if len(sugestao) == 6:
                st.success(f"Sugestão: {sugestao}")
                break
                
    st.divider()
    
    # 3. Banco de Maturação (Com Botão de Salvar aqui agora!)
    st.header("📂 MATURAÇÃO")
    if st.session_state.banco_de_dados:
        df_maturacao = pd.DataFrame(st.session_state.banco_de_dados)
        st.dataframe(df_maturacao[['Jogo', 'Soma']], hide_index=True)
        if st.button("🗑️ Esvaziar Banco"):
            st.session_state.banco_de_dados = []
            st.rerun()
    else:
        st.info("Banco pronto para receber jogos.")

# --- ÁREA CENTRAL (AMBIENTE LIMPO) ---
st.title("🔎 SCANNER DE AUDITORIA")

# Grade de Entrada
cols = st.columns(6)
entradas = []
for i in range(c_qtd):
    with cols[i % 6]:
        num = st.number_input(f"Dezena {i+1}", 1, c_n, key=f"v_{i}")
        entradas.append(num)

meu_jogo = sorted(list(set(entradas)))
soma_u = sum(meu_jogo)
pares = len([n for n in meu_jogo if n % 2 == 0])
impares = 6 - pares

# Botões de Ação Centralizados
col_btn1, col_btn2 = st.columns(2)

with col_btn1:
    executar = st.button("🔍 EXECUTAR SCANNER", use_container_width=True)
with col_btn2:
    salvar = st.button("💾 SALVAR NO BANCO", use_container_width=True)

if executar:
    historico = carregar_historico()
    st.divider()
    
    # Grid de Diagnóstico
    diag1, diag2 = st.columns(2)
    with diag1:
        if c_min <= soma_u <= c_max: st.success(f"✅ SOMA: {soma_u} (IDEAL)")
        else: st.warning(f"⚠️ SOMA: {soma_u} (FORA DO PADRÃO)")
    with diag2:
        if pares in [2, 3, 4]: st.success(f"⚖️ PARIDADE: {pares}P/{impares}Í (EQUILIBRADO)")
        else: st.error(f"❌ PARIDADE: {pares}P/{impares}Í (ALTO RISCO)")

    conflito = False
    for h in historico:
        iguais = set(meu_jogo).intersection(h['nums'])
        if len(iguais) >= 4:
            conflito = True
            st.error(f"🚨 HISTÓRICO: {len(iguais)} acertos no Concurso {h['concurso']} ({h['data']})")
            st.write(f"Números repetidos: {sorted(list(iguais))}")
            
            # Recalibragem Automática
            base = sorted(list(iguais))[:2]
            while True:
                sobra = random.sample([n for n in DEZENAS_ELITE if n not in meu_jogo], 4)
                final = sorted(base + sobra)
                if c_min <= sum(final) <= c_max:
                    st.info(f"💡 **SUGESTÃO DE TROCA ELITE:**")
                    st.success(f"✅ JOGO RECALIBRADO: {final} (Soma: {sum(final)})")
                    break
    
    if not conflito: st.info("💎 JOGO INÉDITO: Nenhuma ocorrência pesada no passado.")

if salvar:
    if len(meu_jogo) < 6:
        st.error("Erro: Insira 6 números diferentes.")
    else:
        st.session_state.banco_de_dados.append({
            "Jogo": str(meu_jogo), "Soma": soma_u, "Status": "Validado"
        })
        st.toast("Jogo enviado para o Banco de Maturação!")
        st.rerun()
