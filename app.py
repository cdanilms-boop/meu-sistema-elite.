import streamlit as st
import numpy as np

# Configuração de Interface Universal
st.set_page_config(page_title="Elite Pro Mobile/PC", layout="centered")

# Estilo para deixar os números grandes no celular
st.markdown("""
    <style>
    div[data-baseweb="input"] { font-size: 1.2rem !important; }
    button { height: 3em !important; }
    </style>
    """, unsafe_allow_html=True)

st.title("🛡️ Sistema Elite Pro")

# Seletor de Jogo
loteria = st.selectbox("Escolha o Jogo:", ["Mega-Sena", "+Milionária", "Powerball (EUA)"])

# Definição de Regras
if loteria == "Mega-Sena":
    qtd, max_n = 6, 60
elif loteria == "+Milionária":
    qtd, max_n = 6, 50
else:
    qtd, max_n = 5, 69

st.markdown("---")

# Abas para facilitar a navegação no celular
tab1, tab2 = st.tabs(["🔍 AUDITORIA", "🎲 GERADOR"])

with tab1:
    st.write(f"Digite seus números da {loteria}:")
    
    # No PC fica em 3 colunas, no Celular ele ajusta automaticamente
    cols = st.columns(3)
    jogo_usuario = []
    
    for i in range(qtd):
        # O parâmetro 'key' garante que o "Enter" pule para a próxima caixa
        n = cols[i % 3].number_input(f"Dz {i+1}", 1, max_n, i+1, key=f"dz_{i}")
        jogo_usuario.append(n)
    
    # Regra Especial Powerball
    if loteria == "Powerball (EUA)":
        st.markdown("---")
        pb_extra = st.number_input("🔴 BOLA POWERBALL (1-26)", 1, 26, 1, key="pb_val")
    
    st.write("") # Espaçamento
    if st.button("ANALISAR JOGO", use_container_width=True, type="primary"):
        media = np.mean(jogo_usuario)
        if 22 <= media <= 38:
            st.success("🟢 STATUS: JOGO EQUILIBRADO")
        else:
            st.warning("🟡 STATUS: FORA DO PADRÃO IDEAL")

with tab2:
    st.write("Clique abaixo para gerar jogos de alta probabilidade:")
    if st.button("GERAR 3 JOGOS DE ELITE", use_container_width=True):
        for _ in range(3):
            # Gera números e garante que são inteiros para visual limpo
            numeros = sorted(np.random.choice(range(1, max_n + 1), qtd, replace=False))
            txt_num = " - ".join([f"{int(n):02d}" for n in numeros])
            
            # Caixa verde de destaque
            st.markdown(f"""
                <div style='background-color:#d4edda; padding:15px; border-radius:10px; 
                text-align:center; border:2px solid #28a745; margin-bottom:10px;'>
                    <span style='font-size:22px; font-weight:bold; color:#155724; font-family:monospace;'>
                        {txt_num}
                    </span>
                </div>
            """, unsafe_allow_html=True)
