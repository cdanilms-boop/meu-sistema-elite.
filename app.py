import streamlit as st
import pandas as pd
from datetime import datetime

# --- CONFIGURAÇÃO DO SISTEMA ---
st.set_page_config(page_title="SISTEMA ELITE PRO - MOTOR", layout="wide")

# Inicialização do Banco de Dados Interno (Memória de Sessão)
if 'banco_de_dados' not in st.session_state:
    st.session_state.banco_de_dados = []

st.title("⚙️ MOTOR ELITE PRO - NÍVEL 2.5")
st.write("Sincronização de Chassi e Memória para Redes Neurais")

# --- 1. SELETOR DE MODALIDADE (O COMBUSTÍVEL) ---
st.sidebar.header("Configurações do Motor")
modalidade = st.sidebar.selectbox(
    "Escolha a Base de Dados:",
    ["Mega-Sena", "Lotofácil", "Powerball (EUA)"]
)

# Definições Técnicas para o Motor
regras = {
    "Mega-Sena": {"min": 150, "max": 220, "qtd": 6, "max_n": 60},
    "Lotofácil": {"min": 170, "max": 220, "qtd": 15, "max_n": 25},
    "Powerball (EUA)": {"min": 130, "max": 200, "qtd": 5, "max_n": 69}
}
conf = regras[modalidade]

# --- 2. ENTRADA DE DADOS PARA ANÁLISE ---
st.subheader(f"📥 Entrada de Dados: {modalidade}")
col1, col2 = st.columns([2, 1])

with col1:
    # Criação dinâmica dos campos conforme a loteria
    entradas = []
    frentes = st.columns(5)
    for i in range(conf['qtd']):
        with frentes[i % 5]:
            num = st.number_input(f"Dezena {i+1}", 1, conf['max_n'], key=f"d_{i}")
            entradas.append(num)

# --- 3. MOTOR DE AUDITORIA (CÁLCULO DE FORÇA) ---
soma = sum(entradas)
ordenados = sorted(entradas)

# Lógica de Score para o Motor
score = 0
if conf['min'] <= soma <= conf['max']:
    score += 70 # Peso maior para a soma ideal
    status_cor = "green"
    veredito = "✅ MOTOR EM ALTA PERFORMANCE"
else:
    score += 20
    status_cor = "red"
    veredito = "⚠️ FALHA DE COMPRESSÃO (SOMA FORA DO ALVO)"

with col2:
    st.markdown(f"""
        <div style="background-color: {status_cor}; padding: 15px; border-radius: 10px; text-align: center; color: white;">
            <h3>{veredito}</h3>
            <h1>Score: {score}%</h1>
            <p>Soma Atual: {soma}</p>
        </div>
    """, unsafe_allow_html=True)

# --- 4. COMANDO DE SALVAMENTO NO BANCO ---
st.divider()
if st.button("💾 REGISTRAR JOGO NO BANCO DE MATURAÇÃO"):
    dados_jogo = {
        "Data/Hora": datetime.now().strftime("%d/%m %H:%M"),
        "Loteria": modalidade,
        "Dezenas": str(ordenados),
        "Soma": soma,
        "Score": f"{score}%"
    }
    st.session_state.banco_de_dados.append(dados_jogo)
    st.success("Dados registrados na memória do motor!")

# --- 5. VISUALIZAÇÃO DO BANCO DE DADOS ---
st.subheader("📂 Banco de Dados de Maturação (Histórico de Testes)")
if st.session_state.banco_de_dados:
    df_memoria = pd.DataFrame(st.session_state.banco_de_dados)
    st.table(df_memoria)
else:
    st.info("O banco de dados está aguardando o primeiro registro.")

st.divider()
st.caption("Próxima etapa: Integração de Redes Neurais e Clusters de Probabilidade.")
