import streamlit as st
import pandas as pd
from datetime import datetime
import random

st.set_page_config(page_title="SISTEMA ELITE PRO - SCANNER DETALHADO", layout="wide")

if 'banco_de_dados' not in st.session_state:
    st.session_state.banco_de_dados = []

# SIMULAÇÃO DE BANCO COMPLETO COM DATAS (Preparando para o CSV real)
@st.cache_data
def carregar_historico_detalhado():
    # Simulando alguns sorteios reais com datas para o seu teste
    return [
        {"concurso": "53", "data": "20/03/1997", "nums": {2, 3, 14, 17, 45, 50}},
        {"concurso": "2600", "data": "10/06/2023", "nums": {5, 9, 32, 44, 49, 57}},
        {"concurso": "2700", "data": "15/01/2024", "nums": {2, 10, 17, 22, 30, 58}}
    ]

st.title("⚙️ MOTOR ELITE PRO - SCANNER DETALHADO")

# --- ENTRADA DE DADOS ---
modalidade = st.sidebar.selectbox("Base de Dados:", ["Mega-Sena"])
c_min, c_max, c_qtd, c_n = 150, 220, 6, 60

st.subheader("🔎 Scanner de Volante Profissional")
cols = st.columns(6)
entradas = []
for i in range(c_qtd):
    with cols[i % 6]:
        num = st.number_input(f"Nº {i+1}", 1, c_n, key=f"n_{i}")
        entradas.append(num)

if st.button("🔍 EXECUTAR SCANNER COM DATAS E DEZENAS"):
    historico = carregar_historico_detalhado()
    meu_jogo = set(entradas)
    soma_u = sum(entradas)
    
    st.markdown("### 📊 Relatório Detalhado de Auditoria")
    
    # Validação de Soma
    if c_min <= soma_u <= c_max:
        st.success(f"✅ Soma {soma_u} aprovada.")
    else:
        st.warning(f"⚠️ Soma {soma_u} fora do padrão (150-220).")

    # Busca Profunda
    encontrou_algo = False
    for h in historico:
        interseccao = meu_jogo.intersection(h['nums'])
        acertos = len(interseccao)
        
        if acertos >= 4:
            encontrou_algo = True
            st.error(f"🚨 ACERTO ENCONTRADO: {acertos} dezenas no Concurso {h['concurso']} em {h['data']}")
            st.write(f"👉 **Números que já saíram:** {sorted(list(interseccao))}")
            st.info(f"💡 Sugestão do Engenheiro: Considere manter {sorted(list(interseccao))[:2]} e rotacionar os outros.")

    if not encontrou_algo:
        st.info("💎 JOGO INÉDITO: Nenhuma coincidência de 4+ números encontrada no histórico.")

st.divider()
# --- SALVAMENTO ---
if st.button("💾 SALVAR PARA MATURAÇÃO"):
    st.session_state.banco_de_dados.append({
        "Data Registro": datetime.now().strftime("%d/%m/%Y %H:%M"),
        "Jogo": str(sorted(entradas)),
        "Soma": soma_u
    })
    st.toast("Registrado!")

st.table(pd.DataFrame(st.session_state.banco_de_dados))
