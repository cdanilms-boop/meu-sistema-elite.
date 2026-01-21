import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
import collections

class SistemaOperacionalDePrecisao:
    def __init__(self, dados):
        self.dados = np.array(dados)
        self.media = np.mean(self.dados)
        self.desvio = np.std(self.dados)

    def calcular_logica_avancada(self):
        # 1. Entropia (Nível de desordem)
        contagem = collections.Counter(self.dados)
        probs = [v / len(self.dados) for v in contagem.values()]
        entropia = stats.entropy(probs)
        
        # 2. Probabilidades de Gauss
        probabilidades = stats.norm.pdf(self.dados, self.media, self.desvio)
        
        return entropia, probabilidades

    def mostrar_painel_visual(self, entropia):
        # Criando o gráfico para não ficar tela em branco
        x = np.linspace(self.media - 4*self.desvio, self.media + 4*self.desvio, 100)
        y = stats.norm.pdf(x, self.media, self.desvio)

        plt.figure(figsize=(12, 6))
        
        # Gráfico da Curva
        plt.subplot(1, 2, 1)
        plt.plot(x, y, color='blue', label='Área de Pertinência')
        plt.fill_between(x, y, alpha=0.2, color='blue')
        plt.scatter(self.dados, [0]*len(self.dados), color='red', label='Sequência Atual')
        plt.title(f"Distribuição Estatística\n(Entropia: {entropia:.4f})")
        plt.legend()

        # Gráfico de Tendência (O que vem a seguir)
        plt.subplot(1, 2, 2)
        plt.plot(self.dados, 'o-', color='green')
        plt.title("Fluxo da Sequência no Tempo")
        plt.grid(True)

        print("Lógica processada. Abrindo painel visual...")
        plt.tight_layout()
        plt.show()

# --- EXECUÇÃO INTEGRADA ---
# Coloque aqui a sua sequência de dados
minha_sequencia = [10, 12, 11, 13, 11, 10, 15, 12, 14, 11]

# O Sistema une o motor com a tela
sistema = SistemaOperacionalDePrecisao(minha_sequencia)
entropia_calculada, probs_calculadas = sistema.calcular_logica_avancada()
sistema.mostrar_painel_visual(entropia_calculada)
