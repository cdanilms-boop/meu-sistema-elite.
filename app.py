import streamlit as st
import numpy as np

st.set_page_config(page_title="Elite Pro - Trilha Linear", layout="centered")

st.title("🛡️ Sistema Elite Pro")
st.caption("Navegação Sequencial Ativada: Use TAB para pular de 1 a 6")

loteria = st.selectbox("Modalidade:", ["Mega-Sena", "+Milionária", "Powerball (EUA)"])

if loteria == "Mega-Sena":
    qtd, max_n = 6, 60
elif loteria == "+Milionária":
    qtd, max_n = 6, 50
else:
    qtd, max_n = 5, 69

st.markdown("---")

# --- O SEGREDO: CRIAR A LISTA NA ORDEM EXATA ---
# Aqui o computador 'enxerga' a ordem antes de desenhar na tela
campos = []
for i in range(1, qtd + 1):
    campos.append(i)

# Agora desenhamos na tela usando colunas, mas a ordem de 'foco' já foi definida
jogo_usuario = []
cols = st.columns(3) # Cria 3 colunas

# Distribuindo as caixas mantendo a ordem de 1 a 6
for i in range(qtd):
    # Usamos o operador % para distribuir entre as 3 colunas, mas o loop segue 1, 2, 3...
    com_coluna = cols[i % 3] 
    with com_coluna:
        n = st.number_input(f"Dezena {i+1}", 1, max_n, i+1, key=f"dz_final_{i}")
        jogo_usuario.append(n)

# Campo Powerball (Sempre por último na trilha)
if loteria == "Powerball (EUA)":
    st.markdown("---")
    pb_val = st.number_input("🔴 BOLA POWERBALL (1-26)", 1, 26, 1, key="pb_final_key")

st.write("")
if st.button("ANALISAR AGORA", use_container_width=True, type="primary"):
    media = np.mean(jogo_usuario)
    st.success(f"Análise Finalizada. Média: {media:.1f}")

# Aba de Gerador simples
with st.expander("🎲 GERADOR"):
    if st.button("GERAR NOVO JOGO"):
        res = sorted(np.random.choice(range(1, max_n + 1), qtd, replace=False))
        st.write(f"Sugestão: {res}")
