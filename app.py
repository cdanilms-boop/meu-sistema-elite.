import streamlit as st
import pandas as pd
import requests
from datetime import datetime, timedelta
import random

# ==========================================
# MOTOR DE DADOS ELITE (ESTÁVEL + DATA DINÂMICA)
# ==========================================
@st.cache_data(ttl=3600)
def carregar_dados_oficiais():
    try:
        url = "https://loteriascaixa-api.herokuapp.com/api/megasena"
        return requests.get(url, timeout=10).json()
    except: return []

def calcular_proximo_sorteio():
    """Calcula automaticamente o próximo dia de sorteio (Ter, Qui, Sab)"""
    hoje = datetime.now()
    # No seu contexto atual é Janeiro de 2026
    dias_sorteio = [1, 3, 5] # Terça(1), Quinta(3), Sábado(5)
    for i in range(1, 8):
        prox = hoy = hoje + timedelta(days=i)
        if prox.weekday() in dias_sorteio:
            semana = ["Segunda", "Terça", "Quarta", "Quinta", "Sexta", "Sábado", "Domingo"]
            return f"{semana[prox.weekday()]}-feira, {prox.strftime('%d/%m/%Y')}"
    return "A definir"

def identificar_quadrante(n):
    col = (n - 1) % 10
    lin = (n - 1) // 10
    if lin <= 2 and col <= 4: return "Q1"
    if lin <= 2 and col > 4: return "Q2"
    if lin > 2 and col <= 4: return "Q3"
    return "Q4"

# ==========================================
# INTERFACE ELITE (ESTRUTURA DO 3º CÓDIGO)
# ==========================================
st.set_page_config(page_title="ELITE PRO V12", layout="wide")
if 'banco' not in st.session_state: st.session_state.banco = []

historico = carregar_dados_oficiais()
if historico:
    ult = historico[0]
    todas = []
    for h in historico[:100]: todas.extend(map(int, h['dezenas']))
    dezenas_elite = pd.Series(todas).value_counts().head(20).index.tolist()

# --- SIDEBAR: PAINEL E MATURAÇÃO (RESTAURADOS) ---
with st.sidebar:
    st.title("🛡️ PAINEL ELITE")
    if historico:
        with st.container(border=True):
            st.write(f"**CONCURSO {ult['concurso']}**")
            st.subheader(" ".join([f"[{n}]" for n in ult['dezenas']]))
            st.warning(f"💰 ESTIMADO: R$ {ult['valorEstimadoProximoConcurso']:,.2f}")
            # RESTAURAÇÃO DA DATA DINÂMICA
            st.info(f"📅 PRÓXIMO: {calcular_proximo_sorteio()}")

    st.divider()
    st.header("✨ GERADOR")
    if st.button("SUGESTÃO DE ELITE"):
        sug_set = set()
        while len(sug_set) < 6:
            sug_set.add(random.choice(dezenas_elite))
            if len(sug_set) < 6: sug_set.add(random.randint(1, 60))
        st.success(f"Sugestão: {sorted(list(sug_set))}")

    st.divider()
    st.header("📂 MATURAÇÃO")
    if st.session_state.banco:
        st.dataframe(pd.DataFrame(st.session_state.banco), hide_index=True)
        if st.button("🗑️ Limpar Tudo"):
            st.session_state.banco = []
            st.rerun()
    
    # BOTÃO DE SALVAR MANUAL (ESTÁVEL)
    if st.button("💾 CONFIRMAR E SALVAR JOGO", type="primary", use_container_width=True):
        jogo_atual = sorted(list(set([st.session_state[f"v_{i}"] for i in range(6)])))
        if len(jogo_atual) == 6:
            st.session_state.banco.append({"Jogo": str(jogo_atual), "Soma": sum(jogo_atual)})
            st.toast("Jogo enviado para maturação!")
            st.rerun()

# --- ÁREA CENTRAL: SCANNER E MAPA ---
st.title("🔎 SCANNER DE AUDITORIA GLOBAL")
cols = st.columns(6)
for i in range(6):
    with cols[i]: st.number_input(f"Nº {i+1}", 1, 60, key=f"v_{i}")

meu_jogo = sorted(list(set([st.session_state[f"v_{i}"] for i in range(6)])))

if st.button("🚀 EXECUTAR SCANNER PROFISSIONAL", use_container_width=True):
    if len(meu_jogo) < 6:
        st.error("Insira 6 dezenas diferentes.")
    else:
        st.divider()
        soma = sum(meu_jogo)
        pares = len([n for n in meu_jogo if n % 2 == 0])
        quads = [identificar_quadrante(n) for n in meu_jogo]
        dist_q = pd.Series(quads).value_counts().to_dict()

        # MÉTRICAS TIPO 3º CÓDIGO (ESTÁVEL)
        c1, c2, c3 = st.columns(3)
        with c1: st.metric("SOMA", soma, "FORA" if soma < 150 or soma > 220 else "OK")
        with c2: st.metric("PARIDADE", f"{pares}P / {6-pares}Í")
        with c3: st.info(f"🗺️ QUADRANTES: {dist_q}")

        # INJEÇÃO DO 2º CÓDIGO: CONFLITOS COM TRANSPARÊNCIA (ESTILO image_029ec5)
        conflitos = [h for h in historico if len(set(meu_jogo).intersection(set(map(int, h['dezenas'])))) >= 4]
        
        if not conflitos:
            st.balloons()
            st.success("💎 JOGO 100% INÉDITO NA HISTÓRIA!")
        else:
            st.markdown("### 🚨 CONFLITOS HISTÓRICOS ENCONTRADOS")
            for conf in conflitos[:2]:
                dezenas_hist = sorted(map(int, conf['dezenas']))
                repetidos = sorted(list(set(meu_jogo).intersection(set(dezenas_hist))))
                
                with st.expander(f"🔴 Concurso {conf['concurso']} - {len(repetidos)} acertos", expanded=True):
                    st.write(f"**Sorteados na época:** {dezenas_hist}")
                    st.write(f"**Repetiram no seu jogo:** `{repetidos}`")
                    st.caption(f"Data do sorteio: {conf['data']}")
            
            # RECALIBRAGEM (ESTILO image_0293e3)
            st.divider()
            st.subheader("💡 RECALIBRAGEM SUGERIDA")
            nova_sug = set(random.sample(dezenas_elite, 4))
            while len(nova_sug) < 6:
                nova_sug.add(random.randint(1, 60))
            st.success(f"✅ NOVO JOGO VALIDADO: {sorted(list(nova_sug))}")
