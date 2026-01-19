import streamlit as st
import numpy as np

# Configuração Universal
st.set_page_config(page_title="Sistema Elite Pro", layout="centered")

# Estilo para destacar onde você está digitando
st.markdown("""
    <style>
    /* Destaca a caixa selecionada com uma cor diferente */
    div[data-baseweb="input"]:focus-within {
        border: 2px solid #28a745 !important;
        background-color: #f0fff0 !important;
    }
    input { font-size: 1.2rem !important; font-weight: bold !important; }
    </style>
    """, unsafe_allow_html=True)

st.title("🛡️ Sistema Elite Pro")
st.info("💡 Dica: Use a tecla **TAB** para pular para a próxima caixa e **ENTER** no final para analisar.")

# Seletor
loteria = st.selectbox("Modalidade:", ["Mega-Sena", "+Milionária", "Powerball (EUA)"])

if loteria == "Mega-Sena":
    qtd, max_n = 6, 60
elif loteria == "+Milionária":
    qtd, max_n = 6, 50
else:
    qtd, max_n = 5, 69

st.markdown("---")

# Criando os campos em uma lista para garantir a ordem
cols = st.columns(3)
jogo_usuario = []

for i in range(qtd):
    # O segredo do 'TAB' funcionar bem é o índice 'i'
    n = cols[i % 3].number_input(f"Dz {i+1}", 1, max_n, i+1, key=f"dz_{i}")
    jogo_usuario.append(n)

# Campo Powerball Extra
if loteria == "Powerball (EUA)":
    st.markdown("---")
    pb_extra = st.number_input("🔴 BOLA POWERBALL (1-26)", 1, 26, 1, key="pb_val")

st.write("") 

# Botão de Ação
if st.button("ANALISAR JOGO AGORA", use_container_width=True, type="primary"):
    media = np.mean(jogo_usuario)
    if 22 <= media <= 38:
        st.success("🟢 STATUS: JOGO DENTRO DO PADRÃO")
    else:
        st.warning("🟡 STATUS: FORA DO PADRÃO IDEAL")

# Aba de Gerador
with st.expander("🎲 GERADOR DE JOGOS"):
    if st.button("GERAR COMBINAÇÕES", use_container_width=True):
        for _ in range(3):
            numeros = sorted(np.random.choice(range(1, max_n + 1), qtd, replace=False))
            txt_num = " - ".join([f"{int(n):02d}" for n in numeros])
            st.markdown(f"<div style='background-color:#d4edda; padding:10px; border-radius:10px; text-align:center; border:1px solid #28a745; margin-bottom:5px;'><b>{txt_num}</b></div>", unsafe_allow_html=True)
