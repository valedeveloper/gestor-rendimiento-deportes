
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg
from matplotlib.ticker import MultipleLocator
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
        """Brinda un resumen de los datos"""

        buffer = io.StringIO()
        self.df.info(buf=buffer)
        salida_info = buffer.getvalue()
        salida_describe = self.df.describe().to_string()
        salida = salida_info + "\n\n" + salida_describe
        return salida
    
    def promedio_puntaje_final(self):
         """Devuevle el puntaje final de la persona"""

         return round(np.mean(self.df["puntaje_final"]),2)

    #Funcionamiento y personalización de la librería Seaborn https://seaborn.pydata.org/generated/seaborn.color_palette.html
    def grafico_circular(self):
        """Hace un gráfico circular del estado de los participantes"""

        conteo_estado_participante = self.df["estado_participante"].value_counts()
        
        fig, ax = plt.subplots(figsize=(5, 5)) 
        colores = sns.color_palette("husl", len(conteo_estado_participante))  
        
        ax.pie(
            conteo_estado_participante, 
            labels=conteo_estado_participante.index, 
            autopct=lambda p: f'{p:.1f}%',  
            colors=colores,
            wedgeprops={'edgecolor': 'white', 'linewidth': 1} #Bordes blancos para la separación
        )

        ax.set_title("Distribución de Clasificación de Participantes", fontsize=14, fontweight="bold") 
        ax.axis("equal") #Círculo redondo
        fig.tight_layout()

        return fig_to_pil(fig)

    def correlation_matrix(self):
        """Correlación de los resultados"""
        
        columnas = ["resultado1", "resultado2", "resultado3"]
        corr = self.df[columnas].corr()

        fig, ax = plt.subplots(figsize=(5,5))
        sns.heatmap(corr, annot=True, fmt=".2f", cmap="crest", linewidths=0.5, ax=ax)
        
        ax.set_title('Matriz de Correlación de Resultados', fontsize=14, fontweight='bold')
        ax.set_xticklabels(columnas, rotation=45, ha='right')
        ax.set_yticklabels(columnas, rotation=0)

        return fig_to_pil(fig)

    def histograma_resultados(self):
        """Histograma de resutlado"""

        fig, ax = plt.subplots(figsize=(5, 5))

        ax.hist(self.df["resultado1"], bins=10, alpha=0.8, label="Resultado 1", color='red', edgecolor='black')
        ax.hist(self.df["resultado2"], bins=10, alpha=0.8, label="Resultado 2", color='blue', edgecolor='black')
        ax.hist(self.df["resultado3"], bins=10, alpha=0.8, label="Resultado 3", color='green', edgecolor='black')

        ax.set_title("Distribución de Resultados por Prueba")
        ax.set_xlabel("Puntaje")
        ax.set_ylabel("Frecuencia")

        ax.yaxis.set_major_locator(MultipleLocator(1)) #Mostrar todos los valores enteros
        ax.legend()
        fig.tight_layout()

        return fig_to_pil(fig)
    
    def histograma_resultados_id(self,id_participante):
        self.df['id'] = self.df['id'].astype(str)
        id = str(id_participante)
        fila_filtrada = self.df[self.df['id'] == id]
        print("FIla filtrada", fila_filtrada)
        if fila_filtrada.empty:
                print(f"No se encontró un participante con ID {id_participante}.")
                return
        
        fig, ax = plt.subplots(figsize=(5, 5))

        ax.hist(self.df["resultado1"], bins=10, alpha=0.8, label="Resultado 1", color='red', edgecolor='black')
        ax.hist(self.df["resultado2"], bins=10, alpha=0.8, label="Resultado 2", color='blue', edgecolor='black')
        ax.hist(self.df["resultado3"], bins=10, alpha=0.8, label="Resultado 3", color='green', edgecolor='black')

        ax.set_title(f"Distribución de Resultados por Prueba de {fila_filtrada["nombre"].values[0]} ")
        ax.set_xlabel("Puntaje")
        ax.set_ylabel("Frecuencia")
        ax.yaxis.set_major_locator(MultipleLocator(1))
        ax.legend()
        fig.tight_layout()

        return fig_to_pil(fig)            
   
    def histograma_dificultades(self):
        fig, ax = plt.subplots(figsize=(5, 5))
        ax.hist(self.df["dificultad1"], bins=10, alpha=0.5, label="Dificultad 1",color='red', edgecolor='black')
        ax.hist(self.df["dificultad2"], bins=10, alpha=0.5, label="Dificultad 2",color='blue', edgecolor='black')
        ax.hist(self.df["dificultad3"], bins=10, alpha=0.5, label="Dificultad 3", color='green', edgecolor='black')

        ax.set_title("Distribución de Dificultad por Prueba")
        ax.set_xlabel("Puntaje")
        ax.set_ylabel("Frecuencia")
        ax.yaxis.set_major_locator(MultipleLocator(1))
        ax.legend()
        fig.tight_layout()

        return fig_to_pil(fig)
    
    def histograma_dificultades_id(self,id_participante):
        self.df['id'] = self.df['id'].astype(str)
        id = str(id_participante)
        fila_filtrada = self.df[self.df['id'] == id]


        fila_filtrada = self.df[self.df['id'] == id]

        if fila_filtrada.empty:
            print(f"No se encontró un participante con ID {id_participante}.")
            return

        fig, ax = plt.subplots(figsize=(5, 5))

        ax.hist(fila_filtrada["dificultad1"], bins=10, alpha=0.5, label="Dificultad 1",color='red', edgecolor='black')
        ax.hist(fila_filtrada["dificultad2"], bins=10, alpha=0.5, label="Dificultad 2",color='blue', edgecolor='black')
        ax.hist(fila_filtrada["dificultad3"], bins=10, alpha=0.5, label="Dificultad 3", color='green', edgecolor='black')

        ax.set_title(f"Distribución de Dificultad por Prueba {fila_filtrada["nombre"].values[0]}")
        ax.set_xlabel("Puntaje")
        ax.set_ylabel("Frecuencia")
        ax.yaxis.set_major_locator(MultipleLocator(1))

        ax.legend()
        fig.tight_layout()
        return fig_to_pil(fig)
   
    def histograma_ponderado_por_prueba(self):
        if "ponderado1" not in self.df.columns:
            self.df["ponderado1"] = self.df["resultado1"] * self.df["dificultad1"]
            self.df["ponderado2"] = self.df["resultado2"] * self.df["dificultad2"]
            self.df["ponderado3"] = self.df["resultado3"] * self.df["dificultad3"]

        #Crera la figura
        fig, ax = plt.subplots(figsize=(5, 5))
        ax.hist(self.df["ponderado1"], bins=10, alpha=0.5, label="Ponderado 1",color='red', edgecolor='black')
        ax.hist(self.df["ponderado2"], bins=10, alpha=0.5, label="Ponderado 2",color='blue', edgecolor='black')
        ax.hist(self.df["ponderado3"], bins=10, alpha=0.5, label="Ponderado 3", color='green', edgecolor='black')

        ax.set_title("Distribución del Puntaje Ponderado por Prueba")
        ax.set_xlabel("Puntaje Ponderado")
        ax.set_ylabel("Frecuencia")
        ax.yaxis.set_major_locator(MultipleLocator(1))

        ax.legend()
        fig.tight_layout()

        return fig_to_pil(fig)
    
    def histograma_ponderado_por_prueba_id(self,id_participante):
        self.df["id"]=self.df["id"].astype(str)
        id=str(id_participante)

        fila_filtrada = self.df[self.df["id"] == id]

        if fila_filtrada.empty:
            print(f"No se encontró un participante con ID {id_participante}.")
            return
        
        #Crea las columnas de puntaje ponderado si no existen
        if "ponderado1" not in self.df.columns:
            self.df["ponderado1"] = self.df["resultado1"] * self.df["dificultad1"]
            self.df["ponderado2"] = self.df["resultado2"] * self.df["dificultad2"]
            self.df["ponderado3"] = self.df["resultado3"] * self.df["dificultad3"]

        #Crear la figura
        fig, ax = plt.subplots(figsize=(5, 5))
        ax.hist(self.df["ponderado1"], bins=10, alpha=0.5, label="Ponderado 1",color='red', edgecolor='black')
        ax.hist(self.df["ponderado2"], bins=10, alpha=0.5, label="Ponderado 2",color='blue', edgecolor='black')
        ax.hist(self.df["ponderado3"], bins=10, alpha=0.5, label="Ponderado 3", color='green', edgecolor='black')

        ax.set_title(f"Distribución del Puntaje Ponderado por Prueba de {fila_filtrada["nombre"].values[0]}")
        ax.set_xlabel("Puntaje Ponderado")
        ax.set_ylabel("Frecuencia")
        ax.legend()
        fig.tight_layout()

        return fig_to_pil(fig)



