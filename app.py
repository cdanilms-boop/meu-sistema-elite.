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
st.set_page_config(page_title="ELITE PRO V5.5", layout="wide")
if 'banco' not in st.session_state: st.session_state.banco = []

historico = carregar_dados_oficiais()
if historico:
    ult = historico[0]
    # Filtro de dezenas quentes (últimos 100 sorteios)
    todas = []
    for h in historico[:100]: todas.extend(map(int, h['dezenas']))
    dezenas_elite = pd.Series(todas).value_counts().head(20).index.tolist()

# --- SIDEBAR (PAINEL DE CONTROLE) ---
with st.sidebar:
    st.title("🛡️ CONTROLE DE ELITE")
    if historico:
        with st.container(border=True):
            st.markdown(f"**CONCURSO {ult['concurso']}**")
            st.subheader(" ".join([f"[{n}]" for n in ult['dezenas']]))
            if ult['acumulou']:
                st.warning(f"💰 ACUMULADO: R$ {ult['valorEstimadoProximoConcurso']:,.2f}")
            st.info(f"📅 PRÓXIMO: {calcular_proximo_sorteio()}")

    st.divider()
    st.header("✨ GERADOR")
    if st.button("SUGESTÃO DE ELITE"):
        sug = sorted(random.sample(dezenas_elite, 3) + random.sample(range(1,61), 3))[:6]
        st.success(f"Sugestão: {sug}")

    st.divider()
    st.header("📂 MATURAÇÃO")
    if st.session_state.banco:
        st.dataframe(pd.DataFrame(st.session_state.banco), hide_index=True)
        if st.button("🗑️ Limpar Tudo"):
            st.session_state.banco = []
            st.rerun()
    
    if st.button("💾 CONFIRMAR E SALVAR JOGO", type="primary", use_container_width=True):
        jogo_atual = sorted([st.session_state[f"v_{i}"] for i in range(6)])
        st.session_state.banco.append({"Jogo": str(jogo_atual), "Soma": sum(jogo_atual)})
        st.toast("Jogo enviado para maturação!")
        st.rerun()

# --- ÁREA CENTRAL (AUDITORIA) ---
st.title("🔎 SCANNER DE AUDITORIA GLOBAL")
st.caption(f"Histórico oficial ativo: {len(historico)} concursos analisados.")

cols = st.columns(6)
for i in range(6):
    with cols[i]:
        st.number_input(f"Nº {i+1}", 1, 60, key=f"v_{i}")

meu_jogo = sorted(list(set([st.session_state[f"v_{i}"] for i in range(6)])))

if st.button("🚀 EXECUTAR SCANNER PROFISSIONAL", use_container_width=True):
    if len(meu_jogo) < 6:
        st.error("Insira 6 dezenas diferentes para auditar.")
    else:
        st.divider()
        soma = sum(meu_jogo)
        pares = len([n for n in meu_jogo if n % 2 == 0])
        
        # 1. Auditoria Estatística
        c1, c2 = st.columns(2)
        with c1:
            if 150 <= soma <= 220: st.success(f"✅ SOMA: {soma} (IDEAL)")
            else: st.warning(f"⚠️ SOMA: {soma} (FORA DO PADRÃO)")
        with c2:
            if pares in [2, 3, 4]: st.success(f"⚖️ PARIDADE: {pares}P/{6-pares}Í (OK)")
            else: st.error(f"❌ PARIDADE: {pares}P/{6-pares}Í (RISCO)")

        # 2. Busca de Conflitos Históricos
        conflitos = [h for h in historico if len(set(meu_jogo).intersection(set(map(int, h['dezenas'])))) >= 4]
        
        if not conflitos:
            st.balloons()
            st.info("💎 JOGO 100% INÉDITO NA HISTÓRIA!")
        else:
            st.markdown("### 🚨 CONFLITOS ENCONTRADOS")
            for conf in conflitos[:3]:
                iguais = sorted(list(set(meu_jogo).intersection(set(map(int, conf['dezenas'])))))
                st.error(f"**{len(iguais)} ACERTOS** no Concurso {conf['concurso']} ({conf['data']})")
                st.write(f"Dezenas repetidas: {iguais}")
            
            # 3. Recalibragem Automática
            st.divider()
            st.subheader("💡 RECALIBRAGEM SUGERIDA")
            nova_sugestao = sorted(list(set(meu_jogo[:2]) | set(random.sample(dezenas_elite, 4))))
            st.success(f"✅ NOVO JOGO VALIDADO: {nova_sugestao} (Soma: {sum(nova_sugestao)})")
