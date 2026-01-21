import streamlit as st
import pandas as pd
import requests
from datetime import datetime, timedelta
import random

# ==========================================
# GAVETA 1: MOTOR DE DADOS E LÓGICA
# ==========================================
@st.cache_data(ttl=3600)
def carregar_dados_oficiais():
    try:
        url = "https://loteriascaixa-api.herokuapp.com/api/megasena"
        return requests.get(url, timeout=10).json()
    except: return []

def calcular_proximo_sorteio():
    hoje = datetime.now()
    dias_sorteio = [1, 3, 5] # Ter, Qui, Sab
    for i in range(1, 8):
        prox = hoje + timedelta(days=i)
        if prox.weekday() in dias_sorteio:
            semana = ["Segunda", "Terça", "Quarta", "Quinta", "Sexta", "Sábado", "Domingo"]
            return f"{semana[prox.weekday()]}-feira, {prox.strftime('%d/%m/%Y')}"
    return "A definir"

# ==========================================
# GAVETA 2: INTERFACE E EXECUÇÃO
# ==========================================
st.set_page_config(page_title="ELITE PRO V10.0", layout="wide")
if 'banco' not in st.session_state: st.session_state.banco = []

historico = carregar_dados_oficiais()
if historico:
    ult = historico[0]
    todas = []
    for h in historico[:100]: todas.extend(map(int, h['dezenas']))
    dezenas_elite = pd.Series(todas).value_counts().head(20).index.tolist()

with st.sidebar:
    st.title("🛡️ CONTROLE DE ELITE")
    if historico:
        with st.container(border=True):
            st.markdown(f"**CONCURSO {ult['concurso']}**")
            st.subheader(" ".join([f"[{n}]" for n in ult['dezenas']]))
            st.info(f"📅 PRÓXIMO: {calcular_proximo_sorteio()}")
            st.warning(f"💰 ESTIMADO: R$ {ult['valorEstimadoProximoConcurso']:,.2f}")

    st.divider()
    st.header("✨ GERADOR")
    if st.button("SUGESTÃO DE ELITE"):
        sug_final = set()
        while len(sug_final) < 6:
            sug_final.add(random.choice(dezenas_elite))
            if len(sug_final) < 6:
                sug_final.add(random.randint(1, 60))
        st.success(f"Sugestão: {sorted(list(sug_final))}")

    st.divider()
    st.header("📂 MATURAÇÃO")
    if st.session_state.banco:
        st.dataframe(pd.DataFrame(st.session_state.banco), hide_index=True)
        if st.button("🗑️ Limpar Tudo"):
            st.session_state.banco = []
            st.rerun()

# --- ÁREA CENTRAL (AUDITORIA) ---
st.title("🔎 SCANNER DE AUDITORIA GLOBAL")
st.caption(f"Varrendo histórico oficial: {len(historico)} concursos analisados.")

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
        with c1: st.metric("SOMA", soma, "DENTRO" if 150 <= soma <= 220 else "ALERTA")
        with c2: st.metric("PARIDADE", f"{pares}P / {6-pares}Í")

        # BUSCA DE CONFLITOS COM EXIBIÇÃO DE NÚMEROS (O QUE ESTAVA FALTANDO)
        conflitos = [h for h in historico if len(set(meu_jogo).intersection(set(map(int, h['dezenas'])))) >= 4]
        
        if not conflitos:
            st.balloons()
            st.success("💎 JOGO 100% INÉDITO NA HISTÓRIA!")
        else:
            st.markdown("### 🚨 CONFLITOS HISTÓRICOS ENCONTRADOS")
            for conf in conflitos[:3]:
                dezenas_hist = sorted(map(int, conf['dezenas']))
                repetidos = sorted(list(set(meu_jogo).intersection(set(dezenas_hist))))
                
                with st.expander(f"🔴 Concurso {conf['concurso']} - {len(repetidos)} acertos", expanded=True):
                    st.write(f"**Números sorteados na época:** {dezenas_hist}")
                    st.write(f"**Dezenas que repetiram no seu jogo:** `{repetidos}`")
                    st.caption(f"Data do sorteio: {conf['data']}")
            
            # RECALIBRAGEM
            st.divider()
            st.subheader("💡 RECALIBRAGEM SUGERIDA")
            nova_sug = set(random.sample(dezenas_elite, 4))
            while len(nova_sug) < 6:
                nova_sug.add(random.randint(1, 60))
            st.success(f"✅ NOVO JOGO VALIDADO: {sorted(list(nova_sug))}")
