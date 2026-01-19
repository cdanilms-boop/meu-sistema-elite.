import streamlit as st
import numpy as np

st.set_page_config(page_title="Elite Pro - Ordem Correta", layout="centered")

# Estilo para as caixas ficarem bem visíveis
st.markdown("""
    <style>
    div[data-baseweb="input"]:focus-within {
        border: 2px solid #28a745 !important;
    }
    input { font-size: 1.5rem !important; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

st.title("🛡️ Sistema Elite Pro")
st.write("Aperte **TAB** para pular: 1 → 2 → 3 → 4 → 5 → 6")

loteria = st.selectbox("Modalidade:", ["Mega-Sena", "+Milionária", "Powerball (EUA)"])

# Define as regras
if loteria == "Mega-Sena":
    qtd, max_n = 6, 60
elif loteria == "+Milionária":
    qtd, max_n = 6, 50
else:
    qtd, max_n = 5, 69

st.markdown("---")

# --- O SEGREDO DA ORDEM ESTÁ AQUI ---
jogo_usuario = []

# Criamos 2 linhas com 3 colunas cada para caber na tela, 
# mas forçamos a ordem de 1 a 6
col1, col2, col3 = st.columns(3)

with col1:
    n1 = st.number_input("Dezena 1", 1, max_n, 1, key="d1")
    n4 = st.number_input("Dezena 4", 1, max_n, 4, key="d4") if qtd >= 4 else None

with col2:
    n2 = st.number_input("Dezena 2", 1, max_n, 2, key="d2")
    n5 = st.number_input("Dezena 5", 1, max_n, 5, key="d5") if qtd >= 5 else None

with col3:
    n3 = st.number_input("Dezena 3", 1, max_n, 3, key="d3")
    n6 = st.number_input("Dezena 6", 1, max_n, 6, key="d6") if qtd >= 6 else None

# Organiza a lista na ordem correta para o cálculo
jogo_usuario = [n for n in [n1, n2, n3, n4, n5, n6] if n is not None]

# Powerball Extra (se aplicável)
if loteria == "Powerball (EUA)":
    st.markdown("---")
    pb_val = st.number_input("🔴 BOLA POWERBALL (1-26)", 1, 26, 1, key="pb_key")

st.write("")
if st.button("ANALISAR AGORA", use_container_width=True, type="primary"):
    media = np.mean(jogo_usuario)
    st.success(f"Análise Concluída! Média: {media:.1f}")

# --- GERADOR ---
with st.expander("🎲 GERADOR"):
    if st.button("GERAR JOGOS"):
        res = sorted(np.random.choice(range(1, max_n + 1), qtd, replace=False))
        st.write(f"Sugerido: {res}")
