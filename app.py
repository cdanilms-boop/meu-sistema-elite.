
import streamlit as st
import pandas as pd
import requests
from datetime import datetime, timedelta
import random

# ==================================================
# MARCO ZERO — SISTEMA ELITE PRO
# Este código representa o último estado confiável
# Tudo que não estiver aqui NÃO é considerado existente
# ==================================================

# -------------------------------
# MOTOR DE DADOS (OFICIAL)
# -------------------------------
@st.cache_data(ttl=3600)
def carregar_dados_oficiais():
    try:
        url = "https://loteriascaixa-api.herokuapp.com/api/megasena"
        return requests.get(url, timeout=10).json()
    except:
        return []

def calcular_proximo_sorteio():
    hoje = datetime.now()
    dias_sorteio = [1, 3, 5]  # Terça, Quinta, Sábado
    for i in range(1, 8):
        prox = hoje + timedelta(days=i)
        if prox.weekday() in dias_sorteio:
            semana = [
                "Segunda", "Terça", "Quarta",
                "Quinta", "Sexta", "Sábado", "Domingo"
            ]
            return f"{semana[prox.weekday()]}-feira, {prox.strftime('%d/%m/%Y')}"
    return "A definir"

# -------------------------------
# CONFIGURAÇÃO DA INTERFACE
# -------------------------------
st.set_page_config(
    page_title="ELITE PRO — MARCO ZERO",
    layout="wide"
)

if "banco" not in st.session_state:
    st.session_state.banco = []

# -------------------------------
# CARREGAMENTO DE DADOS
# -------------------------------
historico = carregar_dados_oficiais()

dezenas_elite = []
if historico:
    ult = historico[0]
    todas = []
    for h in historico[:100]:
        todas.extend(map(int, h["dezenas"]))
    dezenas_elite = (
        pd.Series(todas)
        .value_counts()
        .head(20)
        .index
        .tolist()
    )

# -------------------------------
# SIDEBAR — CONTROLE
# -------------------------------
with st.sidebar:
    st.title("🛡️ CONTROLE ELITE")

    if historico:
        with st.container(border=True):
            st.write(f"**CONCURSO {ult['concurso']}**")
            st.subheader(" ".join([f"[{n}]" for n in ult["dezenas"]]))
            st.info(f"📅 PRÓXIMO: {calcular_proximo_sorteio()}")
            st.warning(
                f"💰 ESTIMADO: R$ {ult['valorEstimadoProximoConcurso']:,.2f}"
            )

    st.divider()
    st.header("✨ GERADOR SIMPLES")

    if st.button("GERAR SUGESTÃO"):
        sugestao = set()
        while len(sugestao) < 6:
            if dezenas_elite:
                sugestao.add(random.choice(dezenas_elite))
            sugestao.add(random.randint(1, 60))
        st.success(f"Sugestão: {sorted(sugestao)}")

    st.divider()
    st.header("📂 MATURAÇÃO")

    if st.session_state.banco:
        st.dataframe(
            pd.DataFrame(st.session_state.banco),
            hide_index=True
        )

        if st.button("🗑️ LIMPAR MATURAÇÃO"):
            st.session_state.banco = []
            st.rerun()

# -------------------------------
# ÁREA PRINCIPAL — AUDITORIA
# -------------------------------
st.title("🔎 SCANNER DE AUDITORIA GLOBAL")

st.caption(
    f"Histórico analisado: {len(historico)} concursos"
)

cols = st.columns(6)
for i in range(6):
    with cols[i]:
        st.number_input(
            f"Nº {i+1}",
            min_value=1,
            max_value=60,
            key=f"v_{i}"
        )

meu_jogo = sorted(
    set(st.session_state[f"v_{i}"] for i in range(6))
)

if st.button("🚀 EXECUTAR AUDITORIA", use_container_width=True):
    if len(meu_jogo) < 6:
        st.error("Informe 6 dezenas diferentes.")
    else:
        st.divider()

        soma = sum(meu_jogo)
        pares = len([n for n in meu_jogo if n % 2 == 0])

        c1, c2 = st.columns(2)
        with c1:
            st.metric(
                "SOMA",
                soma,
                "OK" if 150 <= soma <= 220 else "FORA"
            )
        with c2:
            st.metric(
                "PARIDADE",
                f"{pares} pares / {6-pares} ímpares"
            )

        # CONFLITOS HISTÓRICOS
        conflitos = [
            h for h in historico
            if len(
                set(meu_jogo)
                & set(map(int, h["dezenas"]))
            ) >= 4
        ]

        if not conflitos:
            st.success("💎 JOGO INÉDITO NO HISTÓRICO!")
        else:
            st.markdown("### 🚨 CONFLITOS ENCONTRADOS")
            for conf in conflitos[:3]:
                dezenas_hist = sorted(
                    map(int, conf["dezenas"])
                )
                repetidos = sorted(
                    set(meu_jogo) & set(dezenas_hist)
                )

                with st.expander(
                    f"Concurso {conf['concurso']} "
                    f"({len(repetidos)} repetidas)",
                    expanded=True
                ):
                    st.write(
                        f"Números sorteados: {dezenas_hist}"
                    )
                    st.write(
                        f"Repetidos no seu jogo: {repetidos}"
                    )
                    st.caption(
                        f"Data: {conf['data']}"
                    )
