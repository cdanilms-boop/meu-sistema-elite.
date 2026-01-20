import streamlit as st
import pandas as pd
import requests
from datetime import datetime, timedelta
import random

st.set_page_config(page_title="SISTEMA ELITE PRO - V5.1", layout="wide")

# --- LÓGICA DE DATA DO PRÓXIMO SORTEIO ---
def obter_proximo_sorteio():
    hoje = datetime.now()
    # Dias de sorteio da Mega-Sena: Terça(1), Quinta(3), Sábado(5)
    dias_sorteio = [1, 3, 5]
    proxima_data = hoje
    
    # Busca o próximo dia de sorteio
    for i in range(1, 8):
        candidato = hoje + timedelta(days=i)
        if candidato.weekday() in dias_sorteio:
            proxima_data = candidato
            break
            
    semana = ["Segunda", "Terça", "Quarta", "Quinta", "Sexta", "Sábado", "Domingo"]
    nome_dia = semana[proxima_data.weekday()]
    return f"{nome_dia}-feira, {proxima_data.strftime('%d/%m/%Y')}"

# --- INICIALIZAÇÃO E API ---
if 'banco_de_dados' not in st.session_state:
    st.session_state.banco_de_dados = []

@st.cache_data(ttl=3600)
def carregar_dados_completos():
    try:
        url = "https://loteriascaixa-api.herokuapp.com/api/megasena"
        resposta = requests.get(url, timeout=10)
        dados = resposta.json()
        ultimo = dados[0]
        return {
            "historico": dados,
            "ultimo": {
                "concurso": ultimo['concurso'],
                "data": ultimo['data'],
                "nums": sorted(map(int, ultimo['dezenas'])),
                "acumulou": ultimo['acumulou'],
                "valor": ultimo['valorEstimadoProximoConcurso']
            }
        }
    except:
        return None

dados_api = carregar_dados_completos()
info_proximo = obter_proximo_sorteio()

# --- BARRA LATERAL ATUALIZADA (V5.1) ---
with st.sidebar:
    st.title("🛡️ ELITE PRO 5.1")
    
    if dados_api:
        u = dados_api['ultimo']
        st.subheader("🏁 Último Resultado")
        with st.container(border=True):
            st.markdown(f"**Concurso {u['concurso']}**")
            st.subheader(" ".join([f"[{n}]" for n in u['nums']]))
            if u['acumulou']:
                st.warning(f"💰 ACUMULOU: R$ {u['valor']:,.2f}")
            
            st.divider()
            # O QUE VOCÊ PEDIU: Próximo sorteio detalhado
            st.markdown("📅 **PRÓXIMO SORTEIO:**")
            st.info(f"**{info_proximo}**")

    st.divider()
    if st.button("✨ GERAR SUGESTÃO", use_container_width=True):
        st.code(sorted(random.sample(range(1, 61), 6)))

    st.divider()
    st.header("📂 MATURAÇÃO")
    if st.session_state.banco_de_dados:
        st.table(pd.DataFrame(st.session_state.banco_de_dados))
    
    if st.button("💾 SALVAR ATUAL NA LATERAL", type="primary", use_container_width=True):
        jogo_v = sorted([st.session_state[f"v_{i}"] for i in range(6)])
        st.session_state.banco_de_dados.append({"Jogo": str(jogo_v), "Soma": sum(jogo_v)})
        st.rerun()

# --- ÁREA CENTRAL ---
st.title("🔎 SCANNER DE AUDITORIA GLOBAL")
cols = st.columns(6)
for i in range(6):
    with cols[i]:
        st.number_input(f"Nº {i+1}", 1, 60, key=f"v_{i}")

meu_jogo = sorted([st.session_state[f"v_{i}"] for i in range(6)])
if st.button("🔍 EXECUTAR SCANNER", use_container_width=True):
    st.divider()
    soma = sum(meu_jogo)
    if 150 <= soma <= 220: st.success(f"✅ SOMA: {soma} (DENTRO)")
    else: st.warning(f"⚠️ SOMA: {soma} (FORA)")
    
    # Ineditismo (Varrendo os milhares de jogos que vimos na foto bd1d7f)
    if dados_api:
        conflitos = [j for j in dados_api['historico'] if len(set(meu_jogo).intersection(set(map(int, j['dezenas'])))) >= 4]
        if not conflitos: st.info("💎 JOGO 100% INÉDITO!")
        else: st.error(f"🚨 CONFLITO DETECTADO EM {len(conflitos)} CONCURSOS ANTERIORES.")
