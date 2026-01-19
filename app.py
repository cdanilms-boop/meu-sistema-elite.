import streamlit as st
import numpy as np
from scipy.stats import poisson

# CONFIGURAÇÃO PRO
st.set_page_config(page_title="Sistema Elite Pro", layout="centered") 

st.title("🛡️ Sistema Elite: Auditoria & Gerador")

# 1. SELETOR DE MODALIDADE
loteria = st.selectbox(
    "Escolha a Modalidade:",
    ["Mega-Sena", "+Milionária", "Powerball (EUA)"]
)

st.markdown("---")

# Definição das regras de cada jogo
if loteria == "Mega-Sena":
    qtd_principal, max_num, media_ideal = 6, 60, 30.5
elif loteria == "+Milionária":
    qtd_principal, max_num, media_ideal = 6, 50, 25.5
else: # Powerball (EUA)
    qtd_principal, max_num, media_ideal = 5, 69, 35.0

# --- ABAS ---
tab1, tab2 = st.tabs(["🔍 AUDITORIA", "🎲 GERADOR"])

with tab1:
    st.subheader(f"Análise para {loteria}")
    
    # Caixas para os números principais
    cols = st.columns(qtd_principal)
    jogo_usuario = []
    for i in range(qtd_principal):
        n = cols[i].number_input(f"Dz {i+1}", 1, max_num, i+1, key=f"aud_{i}")
        jogo_usuario.append(n)
    
    # --- REGRA ESPECIAL: CAIXA EXTRA ---
    n_especial = None
    if loteria == "Powerball (EUA)":
        st.markdown("---")
        n_especial = st.number_input("🔴 BOLA POWERBALL (1 a 26)", 1, 26, 1, key="pb_extra")
        st.info("Nota: Na Powerball, você pode repetir um número principal na bola vermelha.")
    
    elif loteria == "+Milionária":
        st.markdown("---")
        st.write("Trevos:")
        c1, c2 = st.columns(2)
        t1 = c1.number_input("Trevo 1", 1, 6, 1)
        t2 = c2.number_input("Trevo 2", 1, 6, 2)

    if st.button("ANALISAR JOGO COMPLETO", use_container_width=True):
        media = np.mean(jogo_usuario)
        if 13 < np.std(jogo_usuario) < 18:
            st.success("🟢 STATUS: JOGO DE ELITE APROVADO")
        else:
            st.warning("⚠️ STATUS: DISTRIBUIÇÃO FORA DO PADRÃO DE HARVARD")

with tab2:
    if st.button("GERAR COMBINAÇÃO DE ELITE", type="primary", use_container_width=True):
        # Gera os principais
        tentativa = sorted(np.random.choice(range(1, max_num + 1), qtd_principal, replace=False))
        num_f = "  -  ".join([f"{int(n):02d}" for n in tentativa])
        
        # Se for Powerball, gera a bola extra também
        if loteria == "Powerball (EUA)":
            pb_extra = np.random.randint(1, 27)
            st.markdown(f"""
            <div style='background-color:#fff3cd;padding:20px;border-radius:10px;text-align:center;border:2px solid #ffecb5;'>
                <h1 style='color:#856404;margin:0;'>{num_f} <span style='color:red;'>[PB: {pb_extra:02d}]</span></h1>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div style='background-color:#d4edda;padding:20px;border-radius:10px;text-align:center;border:2px solid #28a745;'>
                <h1 style='color:#155724;margin:0;'>{num_f}</h1>
            </div>
            """, unsafe_allow_html=True)
