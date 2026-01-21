import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

# ESTA É A CLASSE QUE UNE O CÉREBRO À TELA
class EngineDePrecisao:
    def __init__(self, sequencia):
        self.dados = np.array(sequencia)
        
    def processar_pertinencia(self):
        # Cálculos de Engenharia
        media = np.mean(self.dados)
        desvio = np.std(self.dados)
        # Filtro de Gauss para precisão
        x = np.linspace(media - 4*desvio, media + 4*desvio, 100)
        y = stats.norm.pdf(x, media, desvio)
        return x, y, media

    def renderizar_na_tela(self):
        x, y, media = self.processar_pertinencia()
        
        # Criando a visualização para acabar com o "Branco"
        plt.figure(figsize=(8, 5))
        plt.plot(x, y, color='blue', label='Curva de Probabilidade')
        plt.fill_between(x, y, color='blue', alpha=0.1)
        plt.axvline(media, color='red', linestyle='--', label='Ponto de Pertinência')
        
        plt.title("SISTEMA DE PRECISÃO - ANÁLISE DE SEQUÊNCIAS")
        plt.legend()
        plt.grid(True, alpha=0.3)
        
        # Comando crucial para mostrar a imagem
        print("Renderizando gráfico...")
        plt.show()

# EXECUÇÃO
dados_do_usuario = [10, 12, 11, 13, 11, 10, 15, 12] # Suas sequências aqui
app = EngineDePrecisao(dados_do_usuario)
app.renderizar_na_tela()
