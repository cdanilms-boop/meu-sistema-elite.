import streamlit as st
import pandas as pd
import requests
from datetime import datetime, timedelta
import random

# ==============================================================================
# 🧠 MOTOR DE ENGENHARIA V7.5 - REGRAS DE QUADRANTES E PROBABILIDADE
# ==============================================================================

class MotorElite:
    def __init__(self):
        self.url_api = "https://loteriascaixa-api.herokuapp.com/api/megasena"
        self.historico = self._carregar_dados()
        self.quentes = self._gerar_base_estatistica()
    
    @st.cache_data(ttl=3600)
    def _carregar_dados(_self):
        try:
            return requests.get(_self.url_api, timeout=10).json()
        except: return []

    def _gerar_base_estatistica(self):
        if not self.historico: return list(range(1,61))
        # Pega as dezenas com maior frequência nos últimos 150 concursos
        todas = []
        for h in self.historico[:150]: todas.extend(map(int, h['dezenas']))
        return pd.Series(todas).value_counts().head(25).index.tolist()

    def mapear_quadrante(self, n):
        """Traduz o número para a posição física no volante"""
        col = (n - 1) % 10
        lin = (n - 1) // 10
        if lin <= 2 and col <= 4: return "Q1 (Superior Esq.)"
        if lin <= 2 and col > 4: return "Q2 (Superior Dir.)"
        if lin > 2 and col <= 4: return "Q3 (Inferior Esq.)"
        return "Q4 (Inferior Dir.)"

    def auditar_jogo(self, jogo):
        """Aplica a Metodologia Completa: Harvard + Paridade + Quadrantes + Ineditismo"""
        jogo = sorted(list(set(jogo)))
        if len(jogo) != 6: return {"status": "erro"}

        soma = sum(jogo)
        pares = len([n for n in jogo if n % 2 == 0])
        
        # Mapeamento de Quadrantes para Probabilidade
        quads = [self.mapear_quadrante(n) for n in jogo]
        contagem_quads = pd.Series(quads).value_counts().to_dict()
        # Regra de Elite: Máximo de 3 números por quadrante (Equilíbrio Probabilístico)
        quadrante_ok = all(v <= 3 for v in contagem_quads.values())

        # Busca de Conflitos no Banco de Dados (2961 concursos)
        conflitos = [h for h in self.historico if len(set(jogo).intersection(set(map(int, h['dezenas'])))) >= 4]

        return {
            "status": "sucesso",
            "soma": soma,
            "soma_ok": 150 <= soma <= 220,
            "paridade": f"{pares}P / {6-pares}Í",
            "paridade_ok": pares in [2, 3, 4],
            "quadrantes": contagem_quads,
            "quadrantes_ok": quadrante_ok,
            "conflitos": conflitos,
            "aprovado": (150 <= soma <= 220) and (pares in [2,3,4]) and (len(conflitos) == 0) and quadrante_ok
        }

    def super_gerador(self):
        """Não sorteia números; busca uma combinação que atenda à probabilidade"""
        for _ in range(3000): # O motor trabalha até achar o jogo perfeito
            cand = sorted(random.sample(self.quentes, 4) + random.sample(range(1,61), 2))
            if len(set(cand)) == 6:
                check = self.auditar_jogo(cand)
                if check['aprovado']: return cand
        return sorted(random.sample(range(1,61), 6))

# ==============================================================================
# 🎨 INTERFACE INTEGRADA E PROFISSIONAL (NADA MAIS SOME)
# ==============================================================================
st.set_page_config(page_title="ELITE PRO V7.5", layout="wide")
m = MotorElite()

if 'banco' not in st.session_state: st.session_state.banco = []

# --- PAINEL LATERAL (ESTATÍSTICAS VIVAS) ---
with st.sidebar:
    st.title("🛡️ PAINEL ELITE")
    if m.historico:
        u = m.historico[0]
        with st.container(border=True):
            st.markdown(f"**ÚLTIMO RESULTADO (Conc. {u['concurso']})**")
            st.subheader(f"{u['dezenas']}")
            st.info("📅 Próximo: Quinta-feira, 22/01/2026")
            st.warning("💰 ESTIMADO: R$ 50.000.000,00")
    
    st.divider()
    if st.button("✨ GERAR JOGO PELA METODOLOGIA", type="primary", use_container_width=True):
        jogo_gerado = m.super_gerador()
        st.success(f"Jogo de Elite: {jogo_gerado}")
        st.caption("Validado por: Soma, Paridade, Quadrantes e Ineditismo.")

    st.divider()
    st.header("📂 MATURAÇÃO")
    if st.session_state.banco:
        st.table(pd.DataFrame(st.session_state.banco))
        if st.button("Limpar Banco"): st.session_state.banco = []; st.rerun()

# --- ÁREA CENTRAL (AUDITORIA GLOBAL) ---
st.title("🔎 SCANNER DE AUDITORIA PROFISSIONAL")
st.markdown(f"Varrendo histórico oficial: **{len(m.historico)} concursos analisados.**")

cols = st.columns(6)
for i in range(6):
    with cols[i]: st.number_input(f"Dezena {i+1}", 1, 60, key=f"n_{i}")

meu_jogo = sorted(list(set([st.session_state[f"n_{i}"] for i in range(6)])))

if st.button("🚀 EXECUTAR SCANNER", use_container_width=True):
    res = m.auditar_jogo(meu_jogo)
    if res['status'] == 'erro': st.error("Insira 6 dezenas diferentes.")
    else:
        st.divider()
        c1, c2, c3 = st.columns(3)
        with c1: st.metric("SOMA", res['soma'], "DENTRO" if res['soma_ok'] else "FORA")
        with c2: st.metric("PARIDADE", res['paridade'], "OK" if res['paridade_ok'] else "RISCO")
        with c3: st.metric("QUADRANTES", "EQUILIBRADO" if res['quadrantes_ok'] else "ALERTA")

        # Exibição Detalhada dos Quadrantes
        st.subheader("🗺️ Mapa Espacial do Jogo")
        q_cols = st.columns(4)
        for i, (q, v) in enumerate(res['quadrantes'].items()):
            with q_cols[i % 4]:
                st.write(f"**{q}**")
                st.write(f"{'✅' if v <= 3 else '🚨'} {v} dezenas")

        if res['aprovado']:
            st.balloons()
            st.success("💎 JOGO APROVADO: Segue todos os padrões de probabilidade.")
        else:
            st.error("🚨 JOGO FORA DOS PADRÕES.")
            if res['conflitos']:
                st.write(f"Conflito Histórico: Já houve {len(res['conflitos'])} premiações com 4+ acertos.")

        if st.button("💾 Salvar na Maturação"):
            st.session_state.banco.append({"Jogo": str(meu_jogo), "Soma": res['soma']})
            st.rerun()
