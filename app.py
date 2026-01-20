import streamlit as st
import pandas as pd
import requests
from datetime import datetime, timedelta
import random

# ==============================================================================
# 🔧 PARTE 1: O MOTOR BLINDADO (LÓGICA, MATEMÁTICA E DADOS)
# Nada visual acontece aqui. Apenas processamento bruto.
# ==============================================================================

class MotorElite:
    def __init__(self):
        self.url_api = "https://loteriascaixa-api.herokuapp.com/api/megasena"
        self.historico = self._carregar_dados()
    
    @st.cache_data(ttl=3600)
    def _carregar_dados(_self):
        """Busca os dados na API e blinda contra falhas de conexão."""
        try:
            r = requests.get(_self.url_api, timeout=10)
            if r.status_code == 200:
                return r.json()
            return []
        except:
            return []

    def get_ultimo_resultado(self):
        """Retorna os dados do último sorteio processados."""
        if not self.historico: return None
        u = self.historico[0]
        return {
            "concurso": u['concurso'],
            "data": u['data'],
            "dezenas": sorted([int(d) for d in u['dezenas']]),
            "acumulou": u['acumulou'],
            "valor_acumulado": u['valorEstimadoProximoConcurso']
        }

    def calcular_proximo_data(self):
        """Calcula matematicamente o próximo dia de sorteio."""
        hoje = datetime.now()
        dias_validos = [1, 3, 5] # Ter, Qui, Sab
        for i in range(1, 8):
            futuro = hoje + timedelta(days=i)
            if futuro.weekday() in dias_validos:
                semana = ["Segunda", "Terça", "Quarta", "Quinta", "Sexta", "Sábado", "Domingo"]
                return f"{semana[futuro.weekday()]}-feira, {futuro.strftime('%d/%m/%Y')}"
        return "--"

    def analisar_jogo(self, jogo):
        """
        O CÉREBRO DO SISTEMA.
        Executa todas as validações metodológicas em um único pacote.
        """
        jogo = sorted(list(set(jogo)))
        if len(jogo) != 6: return {"status": "erro", "msg": "Jogo incompleto"}

        soma = sum(jogo)
        pares = len([n for n in jogo if n % 2 == 0])
        
        # Análise de Quadrantes (NOVO!)
        q1 = len([n for n in jogo if n in [1,2,3,4,5,11,12,13,14,15,21,22,23,24,25]])
        q2 = len([n for n in jogo if n in [6,7,8,9,10,16,17,18,19,20,26,27,28,29,30]])
        q3 = len([n for n in jogo if n in [31,32,33,34,35,41,42,43,44,45,51,52,53,54,55]])
        q4 = len([n for n in jogo if n in [36,37,38,39,40,46,47,48,49,50,56,57,58,59,60]])
        distribuicao_quadrantes = f"{q1}-{q2}-{q3}-{q4}"

        # Varredura Histórica (Busca Global)
        conflitos = []
        if self.historico:
            for h in self.historico:
                acertos = len(set(jogo).intersection(set(map(int, h['dezenas']))))
                if acertos >= 4:
                    conflitos.append({
                        "concurso": h['concurso'],
                        "data": h['data'],
                        "acertos": acertos,
                        "dezenas_conflito": sorted(list(set(jogo).intersection(set(map(int, h['dezenas'])))))
                    })

        return {
            "status": "sucesso",
            "soma": soma,
            "soma_status": "IDEAL" if 150 <= soma <= 220 else "FORA",
            "pares": pares,
            "impares": 6 - pares,
            "paridade_status": "OK" if pares in [2, 3, 4] else "RISCO",
            "quadrantes": distribuicao_quadrantes,
            "conflitos": conflitos,
            "inedito": len(conflitos) == 0
        }

    def gerar_sugestao_elite(self):
        """Gera jogo baseado em frequência real."""
        if not self.historico: return sorted(random.sample(range(1,61), 6))
        
        todas = []
        for h in self.historico[:100]: todas.extend(map(int, h['dezenas']))
        freq = pd.Series(todas).value_counts()
        quentes = freq.head(20).index.tolist()
        
        # Algoritmo: 3 Quentes + 3 Aleatórias (Equilíbrio)
        return sorted(list(set(random.sample(quentes, 3) + random.sample(range(1,61), 3))))[:6]


# ==============================================================================
# 🎨 PARTE 2: A LATARIA (INTERFACE GRÁFICA)
# Apenas exibe o que o Motor processou. Não faz cálculos aqui.
# ==============================================================================

st.set_page_config(page_title="SISTEMA ELITE PRO V6.0", layout="wide")

# Inicializa o MOTOR
motor = MotorElite()

# Gerenciamento de Estado (Memória da Sessão)
if 'banco' not in st.session_state: st.session_state.banco = []
if 'ultimo_jogo' not in st.session_state: st.session_state.ultimo_jogo = [0]*6

# --- BARRA LATERAL ---
with st.sidebar:
    st.title("🛡️ CONTROLE ELITE")
    
    # Consulta ao Motor sobre o último resultado
    ultimo = motor.get_ultimo_resultado()
    if ultimo:
        with st.container(border=True):
            st.markdown(f"**CONCURSO {ultimo['concurso']}**")
            st.subheader(" ".join([f"[{n}]" for n in ultimo['dezenas']]))
            if ultimo['acumulou']:
                st.warning(f"💰 ACUMULADO: R$ {ultimo['valor_acumulado']:,.2f}")
            st.info(f"📅 PRÓXIMO: {motor.calcular_proximo_data()}")
    else:
        st.error("Motor desconectado da API.")

    st.divider()
    
    if st.button("✨ GERAR SUGESTÃO DE ELITE"):
        sugestao = motor.gerar_sugestao_elite()
        st.success(f"Sugestão: {sugestao}")
        # Preenche visualmente para facilitar (Opcional)
        st.caption("Jogue estes números no scanner")

    st.divider()
    st.header("📂 MATURAÇÃO")
    if st.session_state.banco:
        st.dataframe(pd.DataFrame(st.session_state.banco), hide_index=True)
        if st.button("🗑️ Limpar Banco"):
            st.session_state.banco = []
            st.rerun()

    if st.button("💾 SALVAR RESULTADO ATUAL", type="primary"):
        # Salva o que estiver na tela
        jogo_salvar = sorted([st.session_state[f"v_{i}"] for i in range(6)])
        res = motor.analisar_jogo(jogo_salvar)
        st.session_state.banco.append({
            "Jogo": str(jogo_salvar), 
            "Soma": res['soma'], 
            "Status": "✅" if res['inedito'] else "❌"
        })
        st.rerun()

# --- ÁREA CENTRAL ---
st.title("🔎 SCANNER DE AUDITORIA 6.0")
st.markdown("### Motor de Análise Preditiva e Histórica")

# Entrada de Dados
cols = st.columns(6)
for i in range(6):
    with cols[i]:
        st.number_input(f"Dezena {i+1}", 1, 60, key=f"v_{i}")

meu_jogo = sorted(list(set([st.session_state[f"v_{i}"] for i in range(6)])))

if st.button("🚀 EXECUTAR SCANNER NO MOTOR", use_container_width=True):
    # CHAMADA AO MOTOR (Aqui a lataria pede ajuda ao motor)
    analise = motor.analisar_jogo(meu_jogo)
    
    if analise['status'] == 'erro':
        st.error(analise['msg'])
    else:
        st.divider()
        
        # Painel de Instrumentos (Soma, Paridade, Quadrantes)
        c1, c2, c3 = st.columns(3)
        with c1:
            lbl = "✅ IDEAL" if analise['soma_status'] == "IDEAL" else "⚠️ ALERTA"
            st.metric("SOMA (Meta: 150-220)", f"{analise['soma']} ({lbl})")
        with c2:
            lbl = "✅ OK" if analise['paridade_status'] == "OK" else "❌ RISCO"
            st.metric("PARIDADE (P/Í)", f"{analise['pares']} / {analise['impares']}", lbl)
        with c3:
            st.metric("DISTRIBUIÇÃO Q1-Q2-Q3-Q4", analise['quadrantes'])
            st.caption("Ideal é distribuir entre os 4 quadrantes.")

        # Relatório de Ineditismo (Vermelho ou Azul)
        st.subheader("Auditoria Histórica")
        if analise['inedito']:
            st.balloons()
            st.success("💎 JOGO APROVADO: 100% INÉDITO NA HISTÓRIA (Motor validou 0 conflitos).")
        else:
            st.error(f"🚨 REPROVADO: Este jogo já teve {len(analise['conflitos'])} premiações relevantes.")
            for c in analise['conflitos'][:3]:
                st.write(f"🔴 **{c['acertos']} Acertos** em {c['data']} (Conc. {c['concurso']}) - Repetidos: {c['dezenas_conflito']}")
            
            # Recalibragem
            st.info("🔧 O Motor sugere recalibrar trocando 2 dezenas.")
