import streamlit as st
import numpy as np

st.set_page_config(page_title="Sistema Elite - Ordem Total", layout="centered")

st.title("🛡️ Sistema Elite Pro")
st.subheader("Navegação Sequencial Garantida")
st.write("Digite o número e aperte **TAB** para o próximo.")

loteria = st.selectbox("Modalidade:", ["Mega-Sena", "+Milionária", "Powerball (EUA)"])

if loteria == "Mega-Sena":
    qtd, max_n = 6, 60
elif loteria == "+Milionária":
    qtd, max_n = 6, 50
else:
    qtd, max_n = 5, 69

st.markdown("---")

# --- A SOLUÇÃO: LISTA VERTICAL PARA ORDEM PERFEITA ---
# Removendo as colunas, o navegador é obrigado a seguir a ordem numérica
jogo_usuario = []

for i in range(1, qtd + 1):
    # Criamos um campo por vez, um embaixo do outro
    n = st.number_input(f"Dezena {i}", 1, max_n, i, key=f"dz_v_{i}")
    jogo_usuario.append(n)

# Campo Powerball (se selecionado)
if loteria == "Powerball (EUA)":
    st.markdown("---")
    pb_val = st.number_input("🔴 BOLA POWERBALL (1-26)", 1, 26, 1, key="pb_v_final")

st.write("")
if st.button("ANALISAR JOGO AGORA", use_container_width=True, type="primary"):
    media = np.mean(jogo_usuario)
    st.success(f"Análise Concluída! Média das dezenas: {media:.1f}")

# Gerador em área separada
with st.expander("🎲 GERADOR DE PALPITES"):
    if st.button("GERAR NOVO"):
        res = sorted(np.random.choice(range(1, max_n + 1), qtd, replace=False))
        st.code(f"Sugestão: {res}")
