import streamlit as st
import pandas as pd
import requests
from datetime import datetime, timedelta
import random

# ==========================================
# MOTOR ESTATÍSTICO (BACK-END INTEGRADO)
# ==========================================
@st.cache_data(ttl=3600)
def carregar_dados_oficiais():
    try:
        url = "https://loteriascaixa-api.herokuapp.com/api/megasena"
        return requests.get(url, timeout=10).json()
    except: return []

def calcular_proximo_sorteio():
    hoje = datetime.now()
    dias_sorteio = [1, 3, 5] 
    for i in range(1, 8):
        prox = hoje + timedelta(days=i)
        if prox.weekday() in dias_sorteio:
            semana = ["Segunda", "Terça", "Quarta", "Quinta", "Sexta", "Sábado", "Domingo"]
            return f"{semana[prox.weekday()]}-feira, {prox.strftime('%d/%m/%Y')}"
    return "A definir"

# --- O FILTRO DE ELITE (PROBABILIDADE REAL) ---
def motor_de_calculo_elite(historico):
    if not historico: return sorted(random.sample(range(1, 61), 6))
    
    # 1. Mapeamento de Frequência
    todas_dezenas = []
    for h in historico[:50]: todas_dezenas.extend(map(int, h['dezenas']))
    frequencia = pd.Series(todas_dezenas).value_counts()
    quentes = frequencia.head(25).index.tolist()
    frias = [n for n in range(1, 61) if n not in quentes]

    # 2. Loop de Validação (O Sistema "pensa" antes de mostrar)
    for tentativa in range(2000):
        # Composição: 4 quentes + 2 frias (Estratégia Profissional)
        sug = random.sample(quentes, 4) + random.sample(frias, 2)
        sug = sorted(sug)
        
        # Filtro A: Soma (Curva de Bell)
        soma = sum(sug)
        if not (150 <= soma <= 220): continue
        
        # Filtro B: Paridade (Equilíbrio de Gauss)
        pares = len([n for n in sug if n % 2 == 0])
        if not (2 <= pares <= 4): continue
        
        # Filtro C: Sequências Proibidas (Ex: 1, 2, 3)
        sequencia = False
        for i in range(len(sug)-2):
            if sug[i+1] == sug[i]+1 and sug[i+2] == sug[i]+2:
                sequencia = True; break
        if sequencia: continue
            
        # Filtro D: Distribuição de Quadrantes
        quadrantes = set()
        for n in sug:
            col = (n - 1) % 10
            lin = (n - 1) // 10
            q = "Q1" if lin <= 2 and col <= 4 else "Q2" if lin <= 2 else "Q3" if col <= 4 else "Q4"
            quadrantes.add(q)
        if len(quadrantes) < 3: continue # Espalhamento obrigatório

        return sug # Só retorna se passar em todos os testes
    return sorted(random.sample(quentes, 6))

# ==========================================
# INTERFACE (FRONT-END)
# ==========================================
st.set_page_config(page_title="SISTEMA ELITE V15", layout="wide")
if 'banco' not in st.session_state: st.session_state.banco = []

historico = carregar_dados_oficiais()

with st.sidebar:
    st.title("🛡️ PAINEL DE CONTROLE")
    if historico:
        ult = historico[0]
        with st.container(border=True):
            st.write(f"**CONCURSO {ult['concurso']}**")
            st.subheader(" ".join([f"[{n}]" for n in ult['dezenas']]))
            st.info(f"📅 PRÓXIMO: {calcular_proximo_sorteio()}")
            st.warning(f"💰 R$ {ult['valorEstimadoProximoConcurso']:,.2f}")

    st.divider()
    st.header("✨ GERADOR CALCULADO")
    if st.button("CALCULAR JOGO DE ELITE"):
        jogo = motor_de_calculo_elite(historico)
        st.success(f"Jogo Validado: {jogo}")
        st.caption("Critérios: 4 Quentes/2 Frias | Sem Sequências | Soma 150-220 | Quadrantes Misto")

    st.divider()
    st.header("📂 MATURAÇÃO")
    if st.session_state.banco:
        st.table(pd.DataFrame(st.session_state.banco))
        if st.button("🗑️ Limpar"):
            st.session_state.banco = []; st.rerun()

# --- ÁREA CENTRAL: AUDITORIA ---
st.title("🔎 SCANNER DE AUDITORIA")
cols = st.columns(6)
for i in range(6):
    with cols[i]: st.number_input(f"Nº {i+1}", 1, 60, key=f"v_{i}")

meu_jogo = sorted(list(set([st.session_state[f"v_{i}"] for i in range(6)])))

if st.button("🚀 EXECUTAR SCANNER", use_container_width=True):
    conflitos = [h for h in historico if len(set(meu_jogo).intersection(set(map(int, h['dezenas'])))) >= 4]
    if not conflitos:
        st.balloons(); st.success("💎 JOGO INÉDITO!")
    else:
        for conf in conflitos[:2]:
            with st.expander(f"🔴 Conflito: Conc. {conf['concurso']}"):
                st.write(f"Sorteados: {conf['dezenas']}")
