import streamlit as st
import pandas as pd
import requests
from datetime import datetime
import random

st.set_page_config(page_title="SISTEMA ELITE PRO - V5.0", layout="wide")

# --- INICIALIZAÇÃO DA MEMÓRIA ---
if 'banco_de_dados' not in st.session_state:
    st.session_state.banco_de_dados = []

# --- FUNÇÃO DE BUSCA AUTOMÁTICA (API ATUALIZADA V5.0) ---
@st.cache_data(ttl=3600)
def carregar_dados_completos():
    try:
        url = "https://loteriascaixa-api.herokuapp.com/api/megasena"
        resposta = requests.get(url, timeout=10)
        dados = resposta.json()
        
        historico = []
        for jogo in dados:
            historico.append({
                "concurso": jogo['concurso'],
                "data": jogo['data'],
                "nums": set(map(int, jogo['dezenas'])),
                "lista_nums": sorted(map(int, jogo['dezenas'])),
                "acumulou": jogo['acumulou'],
                "proximo_estimado": jogo['valorEstimadoProximoConcurso']
            })
        return historico
    except:
        return [{"concurso": "ERRO", "data": "-", "nums": {0}, "lista_nums": [0,0,0,0,0,0], "acumulou": False, "proximo_estimado": 0}]

# Carregamento
historico_global = carregar_dados_completos()
ultimo = historico_global[0]

# Cálculo de Frequência para o Gerador
todas_dezenas = []
for h in historico_global[:60]: # Analisa os últimos 60 dias
    todas_dezenas.extend(list(h['nums']))
freq = pd.Series(todas_dezenas).value_counts()
DEZENAS_ELITE = freq.head(15).index.tolist()

# --- BARRA LATERAL (PAINEL DE RESULTADOS) ---
with st.sidebar:
    st.title("🛡️ ELITE PRO 5.0")
    
    # NOVO CARD DE RESULTADO (O que você pediu!)
    st.subheader("🏁 Último Sorteio")
    with st.container(border=True):
        st.markdown(f"**Concurso {ultimo['concurso']}** ({ultimo['data']})")
        # Mostra as dezenas bonitas
        st.subheader(" ".join([f"[{n}]" for n in ultimo['lista_nums']]))
        
        if ultimo['acumulou']:
            st.warning(f"💰 ACUMULOU!")
            st.write(f"Estimado: R$ {ultimo['proximo_estimado']:,.2f}")
        else:
            st.success("✅ Teve Ganhador!")

    st.divider()
    
    # Gerador Inteligente
    st.header("✨ Gerador")
    if st.button("SUGESTÃO BASEADA EM TENDÊNCIA"):
        sug = sorted(random.sample(DEZENAS_ELITE, 3) + random.sample(range(1,61), 3))[:6]
        st.code(sug)
        
    st.divider()

    # Banco de Maturação
    st.header("📂 MATURAÇÃO")
    if st.session_state.banco_de_dados:
        st.table(pd.DataFrame(st.session_state.banco_de_dados))
        if st.button("🗑️ Limpar"):
            st.session_state.banco_de_dados = []
            st.rerun()
    
    if st.button("💾 SALVAR SCANNER ATUAL", type="primary", use_container_width=True):
        jogo_salvar = sorted([st.session_state[f"v_{i}"] for i in range(6)])
        st.session_state.banco_de_dados.append({"Jogo": str(jogo_salvar), "Soma": sum(jogo_salvar)})
        st.rerun()

# --- ÁREA CENTRAL ---
st.title("🔎 SCANNER DE AUDITORIA GLOBAL")
st.caption(f"Varrendo histórico oficial completo: {len(historico_global)} concursos analisados.")

cols = st.columns(6)
for i in range(6):
    with cols[i]:
        st.number_input(f"Nº {i+1}", 1, 60, key=f"v_{i}")

meu_jogo = sorted([st.session_state[f"v_{i}"] for i in range(6)])
soma_u = sum(meu_jogo)
pares = len([n for n in meu_jogo if n % 2 == 0])

if st.button("🔍 EXECUTAR SCANNER PROFISSIONAL", use_container_width=True):
    st.divider()
    # Auditoria de Harvard e Paridade
    c1, c2 = st.columns(2)
    with c1:
        if 150 <= soma_u <= 220: st.success(f"✅ SOMA: {soma_u} (DENTRO)")
        else: st.warning(f"⚠️ SOMA: {soma_u} (FORA DO PADRÃO)")
    with c2:
        if pares in [2, 3, 4]: st.success(f"⚖️ PARIDADE: {pares}P/{6-pares}Í (OK)")
        else: st.error(f"❌ PARIDADE: {pares}P/{6-pares}Í (RISCO)")

    # Scanner de Ineditismo
    conflitos = [h for h in historico_global if len(set(meu_jogo).intersection(h['nums'])) >= 4]
    if conflitos:
        for c in conflitos[:2]:
            st.error(f"🚨 CONFLITO: {len(set(meu_jogo).intersection(c['nums']))} acertos no Conc. {c['concurso']}")
        # Sugestão de correção
        nova_sug = sorted(list(set(meu_jogo[:2]) | set(random.sample(DEZENAS_ELITE, 4))))
        st.info(f"💡 **RECALIBRAGEM SUGERIDA:** {nova_sug}")
    else:
        st.balloons()
        st.info("💎 JOGO 100% INÉDITO!")
