
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg
import seaborn as sns
import io
from PIL import Image

def fig_to_pil(fig):
    buf = io.BytesIO()
    canvas = FigureCanvasAgg(fig)
    canvas.draw()
    canvas.print_png(buf)
    buf.seek(0)
    return Image.open(buf)

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

    def correlation_matrix(self):
        columnas = ["resultado1", "resultado2", "resultado3"]
        corr = self.df[columnas].corr()

        fig, ax = plt.subplots()
        sns.heatmap(corr, annot=True, cmap='coolwarm', ax=ax)
        ax.set_title('Matriz de Correlación de Resultados')

        return fig_to_pil(fig)
    

    def histograma_resultados(self):
        fig, ax = plt.subplots(figsize=(8, 5))

        ax.hist(self.df["resultado1"], bins=10, alpha=0.5, label="Resultado 1")
        ax.hist(self.df["resultado2"], bins=10, alpha=0.5, label="Resultado 2")
        ax.hist(self.df["resultado3"], bins=10, alpha=0.5, label="Resultado 3")

        ax.set_title("Distribución de Resultados por Prueba")
        ax.set_xlabel("Puntaje")
        ax.set_ylabel("Frecuencia")
        ax.legend()
        fig.tight_layout()

        return fig_to_pil(fig)
    
    def histograma_resultados_id(self,id_participante):
        
        self.df['id'] = self.id['id'].astype(str)
        id = str(id_participante)
        fila_filtrada = self.df[self.df['id'] == id]

        if fila_filtrada.empty:
                print(f"No se encontró un participante con ID {id_participante}.")
                return
        
        fig, ax = plt.subplots(figsize=(8, 5))

        ax.hist(fila_filtrada["resultado1"].values(0), bins=10, alpha=0.5, label="Resultado 1")
        ax.hist(fila_filtrada["resultado2"].values(0), bins=10, alpha=0.5, label="Resultado 2")
        ax.hist(fila_filtrada["resultado3"].values(0), bins=10, alpha=0.5, label="Resultado 3")

        ax.set_title("Distribución de Resultados por Prueba")
        ax.set_xlabel("Puntaje")
        ax.set_ylabel("Frecuencia")
        ax.legend()
        fig.tight_layout()

        return fig_to_pil(fig)            
   
    
    def histograma_dificultades(self):
        fig, ax = plt.subplots(figsize=(8, 5))

        ax.hist(self.df["dificultad1"], bins=10, alpha=0.5, label="Dificultad 1")
        ax.hist(self.df["dificultad2"], bins=10, alpha=0.5, label="Dificultad 2")
        ax.hist(self.df["dificultad3"], bins=10, alpha=0.5, label="Dificultad 3")

        ax.set_title("Distribución de Dificultad por Prueba")
        ax.set_xlabel("Puntaje")
        ax.set_ylabel("Frecuencia")
        ax.legend()
        fig.tight_layout()

        return fig_to_pil(fig)
    
    def histograma_dificultades_id(self,id_participante):
        
        self.df['id'] = self.df['id'].astype(str)
        id_str = str(id_participante)

        fila_filtrada = self.df[self.df['id'] == id_str]

        if fila_filtrada.empty:
            print(f"No se encontró un participante con ID {id_participante}.")
            return

        resultados = [
            fila_filtrada["dificultad1"].values[0],
            fila_filtrada["dificultad2"].values[0],
            fila_filtrada["dificultad3"].values[0]
        ]

        etiquetas = ["Dificultad 1", "Dificultad 2", "Dificultad 3"]

        # Graficar barras
        plt.figure(figsize=(6, 4))
        plt.bar(etiquetas, resultados, color="orange")
        plt.title(f"Nivel de dificultad del Participante {fila_filtrada["nombre"].values[0]}")
        plt.xlabel("Prueba")
        plt.ylabel("Puntaje")
        plt.tight_layout()
        plt.show()         
    
    def histograma_ponderado_por_prueba(self):
        if "ponderado1" not in self.df.columns:
            self.df["ponderado1"] = self.df["resultado1"] * self.df["dificultad1"]
            self.df["ponderado2"] = self.df["resultado2"] * self.df["dificultad2"]
            self.df["ponderado3"] = self.df["resultado3"] * self.df["dificultad3"]

        # Crear la figura
        fig, ax = plt.subplots(figsize=(8, 5))
        ax.hist(self.df["ponderado1"], bins=10, alpha=0.5, label="Ponderado 1")
        ax.hist(self.df["ponderado2"], bins=10, alpha=0.5, label="Ponderado 2")
        ax.hist(self.df["ponderado3"], bins=10, alpha=0.5, label="Ponderado 3")

        ax.set_title("Distribución del Puntaje Ponderado por Prueba")
        ax.set_xlabel("Puntaje Ponderado")
        ax.set_ylabel("Frecuencia")
        ax.legend()
        fig.tight_layout()

        return fig_to_pil(fig)
    
    def histograma_ponderado_por_prueba_id(self,id_participante):

        self.id["id"]=self.df["id"].astype(str)
        id=str(id_participante)

        fila_filtrada = self.df[self.df["id"] == id]

        if fila_filtrada.empty:
            print(f"No se encontró un participante con ID {id_participante}.")
            return
        
        # Crear las columnas de puntaje ponderado si no existen
        if "ponderado1" not in self.df.columns:
            self.df["ponderado1"] = self.df["resultado1"] * self.df["dificultad1"]
            self.df["ponderado2"] = self.df["resultado2"] * self.df["dificultad2"]
            self.df["ponderado3"] = self.df["resultado3"] * self.df["dificultad3"]

        # Crear la figura
        fig, ax = plt.subplots(figsize=(8, 5))
        ax.hist(self.df["ponderado1"], bins=10, alpha=0.5, label="Ponderado 1")
        ax.hist(self.df["ponderado2"], bins=10, alpha=0.5, label="Ponderado 2")
        ax.hist(self.df["ponderado3"], bins=10, alpha=0.5, label="Ponderado 3")

        ax.set_title("Distribución del Puntaje Ponderado por Prueba")
        ax.set_xlabel("Puntaje Ponderado")
        ax.set_ylabel("Frecuencia")
        ax.legend()
        fig.tight_layout()

        return fig_to_pil(fig)







