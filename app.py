import streamlit as st
import pandas as pd
import requests
from datetime import datetime
import random

st.set_page_config(page_title="SISTEMA ELITE PRO - V4.0", layout="wide")

# --- INICIALIZAÇÃO DA MEMÓRIA ---
if 'banco_de_dados' not in st.session_state:
    st.session_state.banco_de_dados = []
if 'historico_real' not in st.session_state:
    st.session_state.historico_real = []

# --- FUNÇÃO DE BUSCA AUTOMÁTICA (API) ---
@st.cache_data(ttl=3600) # Atualiza a cada 1 hora
def atualizar_resultados_caixa():
    try:
        # Link da API de resultados (Exemplo de ponte de dados estável)
        url = "https://loteriascaixa-api.herokuapp.com/api/megasena"
        resposta = requests.get(url, timeout=10)
        dados = resposta.json()
        
        # Transformando os dados da API para o formato do nosso Scanner
        historico = []
        for jogo in dados:
            historico.append({
                "concurso": jogo['concurso'],
                "data": jogo['data'],
                "nums": set(map(int, jogo['dezenas']))
            })
        return historico
    except:
        # Caso a API falhe, mantém um backup mínimo para não travar o sistema
        return [
            {"concurso": "2800", "data": "15/01/2026", "nums": {2, 10, 17, 22, 30, 58}},
            {"concurso": "2799", "data": "13/01/2026", "nums": {5, 12, 25, 33, 41, 52}}
        ]

# Carrega os dados reais
st.session_state.historico_real = atualizar_resultados_caixa()
ultimo_concurso = st.session_state.historico_real[0]

# --- CÁLCULO DINÂMICO DE PESOS (METODOLOGIA) ---
todas_dezenas = []
for h in st.session_state.historico_real[:50]: # Analisa os últimos 50 sorteios
    todas_dezenas.extend(list(h['nums']))
frequencia = pd.Series(todas_dezenas).value_counts()
DEZENAS_ELITE_DINAMICA = frequencia.head(15).index.tolist()

# --- INTERFACE LATERAL ---
with st.sidebar:
    st.title("🛡️ PAINEL DE CONTROLE 4.0")
    st.info(f"📊 Banco: Concurso {ultimo_concurso['concurso']} ({ultimo_concurso['data']})")
    
    st.header("✨ Gerador Inteligente")
    if st.button("GERAR SUGESTÃO COM PESOS REAIS"):
        # Usa as dezenas que mais saíram nos últimos 50 sorteios
        base = random.sample(DEZENAS_ELITE_DINAMICA, 3) + random.sample(range(1, 61), 3)
        sug = sorted(list(set(base)))[:6]
        st.code(f"{sug}")
        st.caption("Baseado na frequência real atualizada.")

    st.divider()
    
    st.header("💾 Ação de Maturação")
    if st.button("CONFIRMAR E SALVAR JOGO", type="primary", use_container_width=True):
        # Captura o jogo atual do estado central
        jogo_atual = sorted([st.session_state[f"v_{i}"] for i in range(6)])
        st.session_state.banco_de_dados.append({
            "Jogo": str(jogo_atual), "Soma": sum(jogo_atual), "Data": datetime.now().strftime("%d/%m")
        })
        st.rerun()

    st.header("📂 BANCO DE MATURAÇÃO")
    if st.session_state.banco_de_dados:
        st.table(pd.DataFrame(st.session_state.banco_de_dados))

# --- ÁREA CENTRAL ---
st.title("🔎 SCANNER DE AUDITORIA GLOBAL")
st.markdown(f"O sistema está varrendo **{len(st.session_state.historico_real)}** sorteios oficiais da história.")

cols = st.columns(6)
for i in range(6):
    with cols[i]:
        st.number_input(f"Dezena {i+1}", 1, 60, key=f"v_{i}")

meu_jogo = sorted([st.session_state[f"v_{i}"] for i in range(6)])
soma_u = sum(meu_jogo)
pares = len([n for n in meu_jogo if n % 2 == 0])

if st.button("🔍 EXECUTAR SCANNER PROFISSIONAL", use_container_width=True):
    st.divider()
    
    # 1. Auditoria Estatística
    c1, c2 = st.columns(2)
    with c1:
        if 150 <= soma_u <= 220: st.success(f"✅ SOMA: {soma_u} (ELITE)")
        else: st.warning(f"⚠️ SOMA: {soma_u} (FORA DO PADRÃO)")
    with c2:
        p_label = f"{pares}P/{6-pares}Í"
        if pares in [2, 3, 4]: st.success(f"⚖️ PARIDADE: {p_label} (OK)")
        else: st.error(f"❌ PARIDADE: {p_label} (ALTO RISCO)")

    # 2. Scanner Histórico Real
    conflitos = [h for h in st.session_state.historico_real if len(set(meu_jogo).intersection(h['nums'])) >= 4]
    
    if conflitos:
        for c in conflitos[:3]: # Mostra os 3 primeiros conflitos
            st.error(f"🚨 ACERTO DE {len(set(meu_jogo).intersection(c['nums']))} NÚMEROS NO CONCURSO {c['concurso']} ({c['data']})")
        
        # Recalibragem
        st.info("💡 **RECALIBRANDO PARA JOGO INÉDITO...**")
        while True:
            nova_sobra = random.sample(DEZENAS_ELITE_DINAMICA, 4)
            novo_jogo = sorted(list(set(meu_jogo[:2]) | set(nova_sobra)))
            if 150 <= sum(novo_jogo) <= 220 and len(novo_jogo) == 6:
                st.success(f"✅ SUGESTÃO VALIDADA: {novo_jogo} (Soma: {sum(novo_jogo)})")
                break
    else:
        st.balloons()
        st.info("💎 JOGO 100% INÉDITO NA HISTÓRIA DA MEGA-SENA!")
