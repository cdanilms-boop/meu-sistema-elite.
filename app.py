import streamlit as st
import pandas as pd
import requests
from datetime import datetime, timedelta
import random

# ==============================================================================
# 🔧 MOTOR INDUSTRIAL V6.3 - BLINDADO CONTRA ERROS
# ==============================================================================

class MotorElite:
    def __init__(self):
        self.url_api = "https://loteriascaixa-api.herokuapp.com/api/megasena"
        self.historico = self._carregar_dados()
        self.dezenas_quentes = self._calcular_quentes()
    
    @st.cache_data(ttl=3600)
    def _carregar_dados(_self):
        try:
            r = requests.get(_self.url_api, timeout=10)
            return r.json() if r.status_code == 200 else []
        except: return []

    def _calcular_quentes(self):
        if not self.historico: return list(range(1,61))
        todas = []
        for h in self.historico[:100]: todas.extend(map(int, h['dezenas']))
        return pd.Series(todas).value_counts().head(20).index.tolist()

    def get_info_completa(self):
        if not self.historico: return None
        u = self.historico[0]
        # Cálculo da Data Próxima
        hoje = datetime.now()
        dias = [1, 3, 5]
        prox_txt = "A definir"
        for i in range(1, 8):
            f = hoje + timedelta(days=i)
            if f.weekday() in dias:
                semana = ["Segunda", "Terça", "Quarta", "Quinta", "Sexta", "Sábado", "Domingo"]
                prox_txt = f"{semana[f.weekday()]}-feira, {f.strftime('%d/%m/%Y')}"
                break
        return {"conc": u['concurso'], "dz": sorted(map(int, u['dezenas'])), "acum": u['acumulou'], "valor": u['valorEstimadoProximoConcurso'], "prox": prox_txt}

    def analisar(self, jogo):
        # SANITIZAÇÃO: Remove repetidos e garante 6 números
        jogo_limpo = sorted(list(set([n for n in jogo if 1 <= n <= 60])))
        if len(jogo_limpo) < 6: return {"status": "erro", "msg": "Insira 6 dezenas diferentes."}
        
        soma = sum(jogo_limpo)
        pares = len([n for n in jogo_limpo if n % 2 == 0])
        conflitos = [h for h in self.historico if len(set(jogo_limpo).intersection(set(map(int, h['dezenas'])))) >= 4]
        
        return {
            "status": "sucesso", "jogo": jogo_limpo, "soma": soma, "soma_ok": 150 <= soma <= 220,
            "pares": pares, "paridade_ok": pares in [2, 3, 4], "conflitos": conflitos, "inedito": len(conflitos) == 0
        }

    def recalibrar(self, jogo_atual):
        # Garante que temos uma base válida mesmo se o jogo original for ruim
        base = list(set(jogo_atual))
        if len(base) < 3: base = random.sample(self.dezenas_quentes, 3)
        else: base = random.sample(base, 3)
        
        for _ in range(300):
            cand = sorted(list(set(base + random.sample(self.dezenas_quentes, 3))))
            if len(cand) == 6:
                res = self.analisar(cand)
                if res['soma_ok'] and res['inedito']: return cand
        return sorted(random.sample(self.dezenas_quentes, 6))

# ==============================================================================
# 🎨 INTERFACE INTEGRADA (NÃO MAIS SUMIRÁ NADA)
# ==============================================================================
st.set_page_config(page_title="ELITE PRO 6.3", layout="wide")
if 'motor' not in st.session_state: st.session_state.motor = MotorElite()
m = st.session_state.motor

# SIDEBAR RESTAURADA
with st.sidebar:
    st.title("🛡️ CONTROLE DE ELITE")
    info = m.get_info_completa()
    if info:
        with st.container(border=True):
            st.markdown(f"**CONCURSO {info['conc']}**")
            st.subheader(f"{info['dz']}")
            if info: st.info(f"📅 PRÓXIMO: {info['prox']}")
            if info['acum']: st.warning(f"💰 ESTIMADO: R$ {info['valor']:,.2f}")
    
    st.divider()
    if st.button("✨ GERAR JOGO METODOLÓGICO"):
        sug = m.recalibrar(random.sample(range(1,61), 6))
        st.success(f"Sugestão: {sug}")

# ÁREA CENTRAL
st.title("🔎 SCANNER DE AUDITORIA")
cols = st.columns(6)
for i in range(6):
    with cols[i]: st.number_input(f"Nº {i+1}", 1, 60, key=f"n_{i}")

meu_jogo = [st.session_state[f"n_{i}"] for i in range(6)]

if st.button("🚀 EXECUTAR AUDITORIA", type="primary", use_container_width=True):
    res = m.analisar(meu_jogo)
    if res['status'] == 'erro':
        st.error(res['msg'])
    else:
        st.divider()
        c1, c2 = st.columns(2)
        c1.metric("SOMA", res['soma'], "DENTRO" if res['soma_ok'] else "FORA")
        c2.metric("PARIDADE", f"{res['pares']}P", "OK" if res['paridade_ok'] else "RISCO")

        if res['inedito']:
            st.success("💎 JOGO INÉDITO!")
        else:
            st.error(f"🚨 CONFLITOS: {len(res['conflitos'])} sorteios anteriores.")
            st.subheader("🛠️ RECALIBRAGEM DO ENGENHEIRO")
            novo = m.recalibrar(res['jogo'])
            st.success(f"✅ JOGO CORRIGIDO: {novo} (Soma: {sum(novo)})")
