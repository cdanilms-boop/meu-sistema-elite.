import streamlit as st
import numpy as np

st.set_page_config(page_title="Elite Pro Compacto", layout="centered")

# Estilo para manter as caixas bonitas e juntas
st.markdown("""
    <style>
    div[data-baseweb="input"] { margin-bottom: -10px; }
    input { font-size: 1.2rem !important; text-align: center; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

st.title("🛡️ Sistema Elite Pro")
st.write("Layout Compacto: Navegação 1-2 → 3-4 → 5-6")

loteria = st.selectbox("Jogo:", ["Mega-Sena", "+Milionária", "Powerball (EUA)"])

if loteria == "Mega-Sena":
    qtd, max_n = 6, 60
elif loteria == "+Milionária":
    qtd, max_n = 6, 50
else:
    qtd, max_n = 5, 69

st.markdown("---")

# --- ORGANIZAÇÃO EM COLUNAS COM SALTO LÓGICO ---
col1, col2, col3 = st.columns(3)

with col1:
    d1 = st.number_input("Dz 1", 1, max_n, 1, key="d1")
    d2 = st.number_input("Dz 2", 1, max_n, 2, key="d2") if qtd >= 2 else None

with col2:
    d3 = st.number_input("Dz 3", 1, max_n, 3, key="d3") if qtd >= 3 else None
    d4 = st.number_input("Dz 4", 1, max_n, 4, key="d4") if qtd >= 4 else None

with col3:
    d5 = st.number_input("Dz 5", 1, max_n, 5, key="d5") if qtd >= 5 else None
    d6 = st.number_input("Dz 6", 1, max_n, 6, key="d6") if qtd >= 6 else None

# Junta os números na ordem correta para a conta de Harvard
jogo = [n for n in [d1, d2, d3, d4, d5, d6] if n is not None]

if loteria == "Powerball (EUA)":
    st.markdown("---")
    pb = st.number_input("🔴 POWERBALL", 1, 26, 1, key="pb_fix")

st.write("")
if st.button("ANALISAR AGORA", use_container_width=True, type="primary"):
    media = np.mean(jogo)
    st.success(f"Análise: Média {media:.1f}")

# Gerador compacto
with st.expander("🎲 GERADOR"):
    if st.button("GERAR"):
        res = sorted(np.random.choice(range(1, max_n + 1), qtd, replace=False))
        st.info(f"Sugestão: {res}")
