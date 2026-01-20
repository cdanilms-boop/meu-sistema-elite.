import streamlit as st
import pandas as pd
from datetime import datetime
import random

st.set_page_config(page_title="SISTEMA ELITE PRO - V3.3", layout="wide")

# Memória do Sistema
if 'banco_de_dados' not in st.session_state:
    st.session_state.banco_de_dados = []

# BANCO HISTÓRICO PARA TESTE DE SCANNER
@st.cache_data
def carregar_historico():
    return [
        {"concurso": "53", "data": "20/03/1997", "nums": {2, 3, 14, 17, 45, 50}},
        {"concurso": "2700", "data": "15/01/2024", "nums": {2, 10, 17, 22, 30, 58}}
    ]

st.title("🛡️ SISTEMA ELITE PRO - VERSÃO 3.3")
st.markdown("---")

# --- ENTRADA DE DADOS ---
c_min, c_max, c_qtd, c_n = 150, 220, 6, 60
st.subheader("1. Configuração do Jogo")
cols = st.columns(6)
entradas = []
for i in range(c_qtd):
    with cols[i % 6]:
        num = st.number_input(f"Nº {i+1}", 1, c_n, key=f"n_{i}")
        entradas.append(num)

# Variáveis de Controle
meu_jogo = sorted(list(set(entradas)))
soma_u = sum(meu_jogo)
pares = len([n for n in meu_jogo if n % 2 == 0])
impares = c_qtd - pares

# --- 2. AUDITORIA TÉCNICA ---
if st.button("🔍 EXECUTAR SCANNER E ANÁLISE COMPLETA"):
    historico = carregar_historico()
    
    st.markdown("### 📊 Relatório de Auditoria Elite")
    col_a, col_b = st.columns(2)
    
    with col_a:
        # Validação de Soma (Harvard)
        if c_min <= soma_u <= c_max:
            st.success(f"✅ SOMA: {soma_u} (Dentro do Padrão)")
        else:
            st.warning(f"⚠️ SOMA: {soma_u} (Fora do Padrão 150-220)")
            
    with col_b:
        # Validação de Paridade
        if pares in [2, 3, 4]:
            st.success(f"⚖️ PARIDADE: {pares}P / {impares}Í (Equilibrado)")
        else:
            st.error(f"❌ PARIDADE: {pares}P / {impares}Í (Desequilibrado)")

    # Scanner de Histórico
    encontrou_conflito = False
    for h in historico:
        interseccao = set(meu_jogo).intersection(h['nums'])
        if len(interseccao) >= 4:
            encontrou_conflito = True
            st.error(f"🚨 CONCURSO ANTIGO DETECTADO: {len(interseccao)} acertos no Concurso {h['concurso']} ({h['data']})")
            st.write(f"Números repetidos: {sorted(list(interseccao))}")
            
            # SUGESTÃO DE TROCA METÓDICA
            manter = sorted(list(interseccao))[:2]
            tentativas = 0
            while tentativas < 1000:
                sobra = random.sample([n for n in range(1, 61) if n not in meu_jogo], 4)
                teste_jogo = sorted(manter + sobra)
                t_soma = sum(teste_jogo)
                t_pares = len([x for x in teste_jogo if x % 2 == 0])
                
                # Só sugere se passar em TODA a metodologia
                if c_min <= t_soma <= c_max and t_pares in [2,3,4]:
                    st.info(f"💡 **Sugestão de Recalibragem:** Mantenha {manter} e substitua o restante.")
                    st.success(f"✅ NOVO JOGO ELITE: {teste_jogo} (Soma: {t_soma} | {t_pares}P/{6-t_pares}Í)")
                    break
                tentativas += 1

    if not encontrou_conflito:
        st.info("💎 JOGO INÉDITO: Nenhuma premiação anterior encontrada.")

st.markdown("---")

# --- 3. SALVAMENTO (CORRIGIDO) ---
if st.button("💾 CONFIRMAR E SALVAR PARA MATURAÇÃO"):
    if len(set(meu_jogo)) < 6:
        st.error("Erro: O jogo precisa de 6 números diferentes.")
    else:
        novo_reg = {
            "Data": datetime.now().strftime("%d/%m/%Y %H:%M"),
            "Jogo": str(meu_jogo),
            "Soma": soma_u,
            "Paridade": f"{pares}P/{impares}Í"
        }
        st.session_state.banco_de_dados.append(novo_reg)
        st.toast("Registrado com sucesso!")

# Tabela de Maturação
if st.session_state.banco_de_dados:
    st.subheader("📂 Banco de Maturação")
    st.table(pd.DataFrame(st.session_state.banco_de_dados))
