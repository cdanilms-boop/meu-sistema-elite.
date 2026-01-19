import streamlit as st
import numpy as np
from scipy.stats import poisson

# --- CONFIGURAÇÃO PRO (VISUAL LIMPO) ---
st.set_page_config(page_title="Sistema Elite Pro", layout="centered") 

st.title("🛡️ Sistema Elite: Inteligência de Loterias")
st.caption("Arquitetura: Harvard v4.0 | Status: Online")

# 1. SELETOR GLOBAL
loteria = st.selectbox(
    "Escolha a Modalidade:",
    ["Mega-Sena", "+Milionária", "Powerball (EUA)"]
)

st.markdown("---")

# Configurações Técnicas
config = {
    "Mega-Sena": {"max": 60, "qtd": 6, "media_h": 30.5},
    "+Milionária": {"max": 50, "qtd": 6, "media_h": 25.5},
    "Powerball (EUA)": {"max": 69, "qtd": 5, "media_h": 35.0}
}

max_num = config[loteria]["max"]
qtd_dezenas = config[loteria]["qtd"]
media_ideal = config[loteria]["media_h"]

# --- INTERFACE POR ABAS ---
tab1, tab2 = st.tabs(["🔍 AUDITORIA TÉCNICA", "🎲 GERADOR DE ELITE"])

with tab1:
    st.write(f"**Analise seu jogo para: {loteria}**")
    cols = st.columns(qtd_dezenas)
    jogo_usuario = []
    
    for i in range(qtd_dezenas):
        num = cols[i].number_input(f"Dz {i+1}", min_value=1, max_value=max_num, value=i+1, key=f"n{i}")
        jogo_usuario.append(num)

    if st.button("ANALISAR POTENCIAL", use_container_width=True):
        media = np.mean(jogo_usuario)
        desvio = np.std(jogo_usuario)
        
        if 13 < desvio < 18 and abs(media - media_ideal) < 8:
            st.success("🟢 JOGO DE ELITE APROVADO")
        else:
            st.error("🔴 JOGO COM BAIXA PROBABILIDADE")
            if media < media_ideal:
                st.info(f"Dica: Tente números mais altos, próximos a {int(media_ideal+10)}.")
            else:
                st.info(f"Dica: Tente números mais baixos, próximos a {int(media_ideal-10)}.")

with tab2:
    st.write("Gere combinações filtradas pela matemática de Harvard.")
    
    if st.button("GERAR JOGOS PERFEITOS", type="primary", use_container_width=True):
        jogos_encontrados = 0
        while jogos_encontrados < 3:
            tentativa = sorted(np.random.choice(range(1, max_num + 1), qtd_dezenas, replace=False))
            if 13 < np.std(tentativa) < 18:
                jogos_encontrados += 1
                jogo_formatado = "  -  ".join([f"{n:02d}" for n in tentativa])
                
                # Visual Limpo (Números em destaque)
                st.markdown(f"""
                <div style='background-color: #d4edda; padding: 20px; border-radius: 10px; margin-bottom: 15px; text-align: center; border: 2px solid #28a745;'>
                    <h1 style='color: #155724; margin:0; font-family: monospace;'>{jogo_formatado}</h1>
                </div>
                """, unsafe_allow_html=True)
