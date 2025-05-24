
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os


import io
from matplotlib.backends.backend_agg import FigureCanvasAgg
from PIL import Image

class DataAnalyzer:
    def __init__(self,data):
         self.df = pd.read_csv(data) 
    
    def fig_to_pil(fig):
        buf = io.BytesIO()
        canvas = FigureCanvasAgg(fig)
        canvas.draw()
        canvas.print_png(buf)
        buf.seek(0)
        return Image.open(buf)

    def summary(self):
        buffer = io.StringIO()
        self.df.info(buf=buffer)
        salida_info = buffer.getvalue()
        salida_describe = self.df.describe().to_string()
        salida = salida_info + "\n\n" + salida_describe
        return salida
    
    def promedio_puntaje_final(self):
         return np.mean(self.df["puntaje_final"])

    def grafico_circular(self):
            plt.figure(figsize=(8, 6))
            conteo_estado_participante = self.df["estado_participante"].value_counts()
            plt.pie(
                conteo_estado_participante, 
                labels=conteo_estado_participante.index, 
                autopct='%1.1f%%', 
                colors=sns.color_palette("pastel") 
            )

            plt.title("Distribución de Clasificación Participantes")
            plt.axis("equal")  # Hace que el gráfico sea un círculo perfecto
            plt.tight_layout()
            plt.show()         

    #- Matriz de correlación de los puntajes (pandas)
    #Resultados por prueba en un histograma con matplotlib - Nivel de dificultad aplicado en cada prueba en un histograma con matplotlib - 
    #Puntaje ponderado por prueba en un histograma con matplotlib


data=DataAnalyzer("participantes.csv")
# data.grafico_circular()
data.correlation_matrix()