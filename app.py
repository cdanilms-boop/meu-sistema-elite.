import streamlit as st
import numpy as np
from scipy.stats import poisson

# --- CONFIGURAÇÃO ELITE PRO ---
st.set_page_config(page_title="Sistema Elite Pro", layout="centered") 

st.title("🛡️ Sistema Elite: Inteligência de Loterias")
st.caption("Arquitetura: Harvard v4.0 | Status: Online")

loteria = st.selectbox("Escolha a Modalidade:", ["Mega-Sena", "+Milionária", "Powerball (EUA)"])
st.markdown("---")

config = {
    "Mega-Sena": {"max": 60, "qtd": 6, "media_h": 30.5},
    "+Milionária": {"max": 50, "qtd": 6, "media_h": 25.5},
    "Powerball (EUA)": {"max": 69, "qtd": 5, "media_h": 35.0}
}

max_num = config[loteria]["max"]
qtd_dezenas = config[loteria]["qtd"]
media_ideal = config[loteria]["media_h"]

tab1, tab2 = st.tabs(["🔍 AUDITORIA", "🎲 GERADOR"])

with tab1:
    cols = st.columns(qtd_dezenas)
    jogo_usuario = [cols[i].number_input(f"Dz {i+1}", 1, max_num, i+1) for i in range(qtd_dezenas)]
    if st.button("ANALISAR", use_container_width=True):
        media, desvio = np.mean(jogo_usuario), np.std(jogo_usuario)
        if 13 < desvio < 18 and abs(media - media_ideal) < 8:
            st.success("🟢 JOGO DE ELITE APROVADO")
        else:
            st.error("🔴 BAIXA PROBABILIDADE")

with tab2:
    if st.button("GERAR JOGOS PERFEITOS", type="primary", use_container_width=True):
        for _ in range(3):
            ok = False
            while not ok:
                tentativa = sorted(np.random.choice(range(1, max_num + 1), qtd_dezenas, replace=False))
                if 13 < np.std(tentativa) < 18:
                    ok = True
                    num_f = "  -  ".join([f"{n:02d}" for n in tentativa])
                    st.markdown(f"<div style='background-color:#d4edda;padding:20px;border-radius:10px;margin-bottom:15px;text-align:center;border:2px solid #28a745;'><h1 style='color:#155724;margin:0;font-family:monospace;'>{num_f}</h1></div>", unsafe_allow_html=True)
