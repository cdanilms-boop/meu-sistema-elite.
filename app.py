import streamlit as st
import pandas as pd
import requests
from datetime import datetime, timedelta
import random

# 1. MOTOR DE DADOS (Não mexe na tela)
@st.cache_data(ttl=3600)
def carregar_dados_caixa():
    try:
        url = "https://loteriascaixa-api.herokuapp.com/api/megasena"
        dados = requests.get(url, timeout=10).json()
        return dados
    except:
        return []

def calcular_proximo_sorteio():
    hoje = datetime.now()
    dias = [1, 3, 5] # Terça, Quinta, Sábado
    for i in range(1, 8):
        prox = hoje + timedelta(days=i)
        if prox.weekday() in dias:
            semana = ["Segunda", "Terça", "Quarta", "Quinta", "Sexta", "Sábado", "Domingo"]
            return f"{semana[prox.weekday()]}-feira, {prox.strftime('%d/%m/%Y')}"
    return "A definir"

# 2. CONFIGURAÇÃO DA LATARIA
st.set_page_config(page_title="ELITE PRO V5.3", layout="wide")

# Inicialização de memória
if 'banco' not in st.session_state: st.session_state.banco = []

# Carga de dados
historico_real = carregar_dados_caixa()
if historico_real:
    ultimo = historico_real[0]
    # Cálculo de dezenas quentes para o Gerador
    todas = []
    for h in historico_real[:50]: todas.extend(map(int, h['dezenas']))
    dezenas_quentes = pd.Series(todas).value_counts().head(15).index.tolist()

# --- BARRA LATERAL (PAINEL DE CONTROLE) ---
with st.sidebar:
    st.title("🛡️ PAINEL DE CONTROLE")
    
    if historico_real:
        with st.container(border=True):
            st.markdown(f"**CONCURSO {ultimo['concurso']}**")
            st.subheader(" ".join([f"[{n}]" for n in ultimo['dezenas']]))
            if ultimo['acumulou']:
                st.warning(f"💰 ACUMULADO: R$ {ultimo['valorEstimadoProximoConcurso']:,.2f}")
            st.info(f"📅 Próximo: {calcular_proximo_sorteio()}")

    st.divider()
    
    # VOLTOU: Gerador de Sugestões
    st.header("✨ Gerador Elite")
    if st.button("GERAR SUGESTÃO INTELIGENTE"):
        sug = sorted(random.sample(dezenas_quentes, 3) + random.sample(range(1,61), 3))[:6]
        st.success(f"Sugestão: {sug}")

    st.divider()
    
    # VOLTOU: Banco de Maturação
    st.header("📂 MATURAÇÃO")
    if st.session_state.banco:
        st.dataframe(pd.DataFrame(st.session_state.banco), hide_index=True)
        if st.button("🗑️ Limpar"):
            st.session_state.banco = []
            st.rerun()
    
    if st.button("💾 SALVAR JOGO ATUAL", type="primary", use_container_width=True):
        jogo_v = sorted([st.session_state[f"v_{i}"] for i in range(6)])
        st.session_state.banco.append({"Jogo": str(jogo_v), "Soma": sum(jogo_v)})
        st.toast("Jogo salvo com sucesso!")
        st.rerun()

# --- ÁREA CENTRAL (EXECUÇÃO DO SCANNER) ---
st.title("🔎 SCANNER DE AUDITORIA GLOBAL")
st.caption(f"Analisando histórico oficial: {len(historico_real)} concursos carregados.")

# Entrada de números
cols = st.columns(6)
for i in range(6):
    with cols[i]:
        st.number_input(f"Nº {i+1}", 1, 60, key=f"v_{i}")

meu_jogo = sorted(list(set([st.session_state[f"v_{i}"] for i in range(6)])))

if st.button("🚀 EXECUTAR SCANNER PROFISSIONAL", use_container_width=True):
    if len(meu_jogo) < 6:
        st.error("Por favor, insira 6 números diferentes.")
    else:
        st.divider()
        soma = sum(meu_jogo)
        pares = len([n for n in meu_jogo if n % 2 == 0])
        
        # Auditoria Visual
        c1, c2 = st.columns(2)
        with c1:
            if 150 <= soma <= 220: st.success(f"✅ SOMA: {soma} (IDEAL)")
            else: st.warning(f"⚠️ SOMA: {soma} (FORA DO PADRÃO)")
        with c2:
            if pares in [2, 3, 4]: st.success(f"⚖️ PARIDADE: {pares}P/{6-pares}Í (OK)")
            else: st.error(f"❌ PARIDADE: {pares}P/{6-pares}Í (ALTO RISCO)")

        # VOLTOU: Verificação de Ineditismo Global
        conflitos = [h for h in historico_real if len(set(meu_jogo).intersection(set(map(int, h['dezenas'])))) >= 4]
        
        if not conflitos:
            st.balloons()
            st.info("💎 JOGO 100% INÉDITO NA HISTÓRIA!")
        else:
            for conf in conflitos[:2]:
                st.error(f"🚨 CONCURSO {conf['concurso']} ({conf['data']}): {len(set(meu_jogo).intersection(set(map(int, conf['dezenas']))))} ACERTOS.")
            
            # Recalibragem Automática
            nova_sug = sorted(list(set(meu_jogo[:2]) | set(random.sample(dezenas_quentes, 4))))
            st.info(f"💡 **SUGESTÃO DE TROCA:** {nova_sug}")
