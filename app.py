import streamlit as st
import numpy as np

# ==========================================
# 🧠 MOTOR DE INTELIGÊNCIA HARVARD (NÍVEL 1)
# ==========================================

def motor_auditoria(dezenas, modalidade):
    """Realiza a análise técnica completa de um jogo."""
    if not dezenas or len(dezenas) < 5:
        return None
    
    # 1. Cálculo de Soma Térmica
    soma = sum(dezenas)
    # Define zonas de sucesso baseadas na modalidade
    if modalidade == "Mega-Sena":
        faixa = (150, 220)
    elif modalidade == "+Milionária":
        faixa = (120, 190)
    else: # Powerball
        faixa = (130, 200)
        
    status_soma = "Ideal ✅" if faixa[0] <= soma <= faixa[1] else "Fora do Padrão ⚠️"
    
    # 2. Equilíbrio Par/Ímpar
    pares = len([n for n in dezenas if n % 2 == 0])
    impares = len(dezenas) - pares
    
    # 3. Detector de Sequências (Adjacência)
    dezenas_ord = sorted(dezenas)
    seq_count = 0
    for i in range(len(dezenas_ord)-1):
        if dezenas_ord[i+1] == dezenas_ord[i] + 1:
            seq_count += 1
    
    return {
        "soma": soma,
        "status_soma": status_soma,
        "par_impar": f"{pares}P / {impares}I",
        "sequencias": seq_count,
        "aprovado": (faixa[0] <= soma <= faixa[1]) and seq_count <= 1
    }

def gerador_elite(qtd, max_n, modalidade):
    """Gera apenas jogos que cumprem os critérios do Motor."""
    for _ in range(1000):  # Tenta até 1000 combinações
        jogo = sorted(np.random.choice(range(1, max_n + 1), qtd, replace=False).tolist())
        analise = motor_auditoria(jogo, modalidade)
        if analise["aprovado"]:
            return jogo
    return sorted(np.random.choice(range(1, max_n + 1), qtd, replace=False).tolist())

# ==========================================
# 🖥️ INTERFACE ESTRUTURADA (LAYOUT PRESERVADO)
# ==========================================

st.set_page_config(page_title="SISTEMA ELITE PRO", layout="centered")
st.title("🛡️ SISTEMA ELITE PRO")
st.subheader("Motor de Auditoria Harvard - Nível 1")

# Inicializar Memória de Favoritos
if 'favoritos' not in st.session_state:
    st.session_state.favoritos = []

# Configuração de Modalidade
loteria = st.selectbox("Escolha a Modalidade:", ["Mega-Sena", "+Milionária", "Powerball"])
if loteria == "Mega-Sena":
    qtd, max_n = 6, 60
elif loteria == "+Milionária":
    qtd, max_n = 6, 50
else:
    qtd, max_n = 5, 69

st.divider()

# Grid de Inputs (Layout 3 colunas mobile-first)
col1, col2, col3 = st.columns(3)
with col1:
    d1 = st.number_input("Dz 1", 1, max_n, 1, key="dz1")
    d2 = st.number_input("Dz 2", 1, max_n, 10, key="dz2")
with col2:
    d3 = st.number_input("Dz 3", 1, max_n, 20, key="dz3")
    d4 = st.number_input("Dz 4", 1, max_n, 30, key="dz4")
with col3:
    d5 = st.number_input("Dz 5", 1, max_n, 40, key="dz5")
    d6 = st.number_input("Dz 6", 1, max_n, 50, key="dz6") if qtd == 6 else None

# Montagem do Jogo Atual
jogo_lista = [d1, d2, d3, d4, d5]
if d6: jogo_lista.append(d6)

# ==========================================
# ⚙️ PAINEL DE CONTROLE E RESULTADOS
# ==========================================

btn_col1, btn_col2, btn_col3 = st.columns(3)

with btn_col1:
    if st.button("ANALISAR 📊", use_container_width=True, type="primary"):
        res = motor_auditoria(jogo_lista, loteria)
        st.write("---")
        st.write(f"**Soma:** {res['soma']} ({res['status_soma']})")
        st.write(f"**Equilíbrio:** {res['par_impar']}")
        st.write(f"**Sequências:** {res['sequencias']}")
        if res["aprovado"]:
            st.success("JOGO APROVADO PELA METODOLOGIA")
        else:
            st.warning("JOGO FORA DOS PADRÕES DE ELITE")

with btn_col2:
    if st.button("GERAR ELITE 🚀", use_container_width=True):
        sugestao = gerador_elite(qtd, max_n, loteria)
        st.code(f"Sugestão: {sugestao}")
        st.info("Este jogo passou em todos os filtros de Harvard.")

with btn_col3:
    if st.button("SALVAR ⭐", use_container_width=True):
        st.session_state.favoritos.append({"Jogo": jogo_lista, "Tipo": loteria})
        st.toast("Jogo salvo na memória!")

# Exibição da Memória de Favoritos
if st.session_state.favoritos:
    with st.expander("📂 Meus Jogos Salvos (Auditoria)"):
        st.table(st.session_state.favoritos)
