import streamlit as st
import pandas as pd
import requests
from datetime import datetime, timedelta
import random

# --- GAVETA 1: INTELIGÊNCIA E DADOS ---
@st.cache_data(ttl=3600)
def carregar_dados_caixa():
    try:
        url = "https://loteriascaixa-api.herokuapp.com/api/megasena"
        return requests.get(url, timeout=10).json()
    except: return []

def calcular_proximo_sorteio():
    hoje = datetime.now()
    dias = [1, 3, 5] # Ter, Qui, Sab
    for i in range(1, 8):
        prox = hoje + timedelta(days=i)
        if prox.weekday() in dias:
            semana = ["Segunda", "Terça", "Quarta", "Quinta", "Sexta", "Sábado", "Domingo"]
            return f"{semana[prox.weekday()]}, {prox.strftime('%d/%m')}"
    return "A definir"

# --- GAVETA 2: INTERFACE ---
st.set_page_config(page_title="ELITE PRO V5.4", layout="wide")
if 'banco' not in st.session_state: st.session_state.banco = []

hist_real = carregar_dados_caixa()
dezenas_quentes = []
if hist_real:
    ultimo = hist_real[0]
    # Pega as 20 dezenas mais frequentes dos últimos 100 jogos para sugestões fortes
    todas = []
    for h in hist_real[:100]: todas.extend(map(int, h['dezenas']))
    dezenas_quentes = pd.Series(todas).value_counts().head(20).index.tolist()

# --- SIDEBAR ---
with st.sidebar:
    st.title("🛡️ PAINEL ELITE")
    if hist_real:
        with st.container(border=True):
            st.markdown(f"**CONCURSO {ultimo['concurso']}**")
            st.subheader(" ".join([f"[{n}]" for n in ultimo['dezenas']]))
            if ultimo['acumulou']:
                st.warning(f"💰 R$ {ultimo['valorEstimadoProximoConcurso']:,.2f}")
            st.info(f"📅 Próximo: {calcular_proximo_sorteio()}")

    st.divider()
    st.header("✨ Gerador")
    if st.button("SUGESTÃO DE ELITE"):
        sug = sorted(random.sample(dezenas_quentes, 4) + random.sample(range(1,61), 2))[:6]
        st.success(f"Sugestão: {sug}")

    st.divider()
    st.header("📂 MATURAÇÃO")
    if st.session_state.banco:
        st.dataframe(pd.DataFrame(st.session_state.banco), hide_index=True)
        if st.button("🗑️ Limpar Banco"):
            st.session_state.banco = []
            st.rerun()

    if st.button("💾 SALVAR NO BANCO", type="primary", use_container_width=True):
        j_atual = sorted(list(set([st.session_state[f"v_{i}"] for i in range(6)])))
        if len(j_atual) == 6:
            st.session_state.banco.append({"Jogo": str(j_atual), "Soma": sum(j_atual)})
            st.rerun()

# --- ÁREA CENTRAL ---
st.title("🔎 SCANNER DE AUDITORIA GLOBAL")
st.caption(f"Histórico Oficial: {len(hist_real)} concursos analisados.")

cols = st.columns(6)
for i in range(6):
    with cols[i]:
        st.number_input(f"Nº {i+1}", 1, 60, key=f"v_{i}")

meu_jogo = sorted(list(set([st.session_state[f"v_{i}"] for i in range(6)])))

if st.button("🚀 EXECUTAR SCANNER PROFISSIONAL", use_container_width=True):
    if len(meu_jogo) < 6:
        st.error("Insira 6 dezenas diferentes.")
    else:
        st.divider()
        soma = sum(meu_jogo)
        pares = len([n for n in meu_jogo if n % 2 == 0])
        
        c1, c2 = st.columns(2)
        with c1:
            if 150 <= soma <= 220: st.success(f"✅ SOMA: {soma} (IDEAL)")
            else: st.warning(f"⚠️ SOMA: {soma} (FORA DO PADRÃO)")
        with c2:
            if pares in [2, 3, 4]: st.success(f"⚖️ PARIDADE: {pares}P/{6-pares}Í (EQUILIBRADO)")
            else: st.error(f"❌ PARIDADE: {pares}P/{6-pares}Í (ALTO RISCO)")

        # Lógica de Ineditismo com Recalibragem Cirúrgica
        conflitos = []
        for h in hist_real:
            sorteados = set(map(int, h['dezenas']))
            iguais = set(meu_jogo).intersection(sorteados)
            if len(iguais) >= 4:
                conflitos.append({"conc": h['concurso'], "data": h['data'], "nums": iguais})

        if not conflitos:
            st.balloons()
            st.info("💎 JOGO 100% INÉDITO NA HISTÓRIA!")
        else:
            for c in conflitos[:3]:
                st.error(f"🚨 CONCURSO {c['conc']} ({c['data']}): {len(c['nums'])} ACERTOS -> {sorted(list(c['nums']))}")
            
            # RECALIBRAGEM FORTE (Mantém a base, troca o conflito)
            st.markdown("### 🛠️ RECALIBRAGEM DE PRECISÃO:")
            # Tenta gerar uma sugestão que resolva o problema da soma e do conflito
            tentativas = 0
            while tentativas < 100:
                # Mantém 2 ou 3 números originais que não estavam no conflito principal se possível
                base_limpa = [n for n in meu_jogo if n not in conflitos[0]['nums']]
                if len(base_limpa) < 2: base_limpa = meu_jogo[:2]
                
                complemento = random.sample(dezenas_quentes, 6 - len(base_limpa))
                final = sorted(list(set(base_limpa + complemento)))[:6]
                
                if 150 <= sum(final) <= 220:
                    st.success(f"✅ SUGESTÃO VALIDADA: {final} (Soma: {sum(final)})")
                    break
                tentativas += 1
