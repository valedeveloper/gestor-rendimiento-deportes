import random 
import pandas as pd
import os
import csv
class Participante:
    def __init__(self,id,nombre,resultados):
        self.id=id
        self.nombre=nombre
        self.resultados=[float(r) for r in resultados]
        self.dificultades = [round(random.uniform(1.0, 1.3),2) for _ in range(3)]
        self.resultados=resultados
        

    def calcular_puntaje_final(self):
        """Calcula el puntaje del participante"""

        #The zip() function returns a zip object, which is an iterator of tuples where the first item in each passed iterator is paired together - https://www.w3schools.com/python/ref_func_zip.asp
        suma_ponderada=sum(resultado*dificultad for resultado,dificultad in zip(self.resultados,self.dificultades))
        suma_dificultades=sum(self.dificultades)
        return round(suma_ponderada/suma_dificultades,1)
    

    def clasificar_puntaje(self):
        """Clasifica segun puntaje"""
        puntaje_participante=self.calcular_puntaje_final()
        
        if puntaje_participante>=70:
            return "Clasificó"
        
        return "No clasificó"
        
    
    def reporte_participante(self):
        return {
                "id": self.id,
                "nombre": self.nombre,
                "resultado1": self.resultados[0],
                "resultado2": self.resultados[1],
                "resultado3": self.resultados[2],
                "dificultad1": self.dificultades[0],
                "dificultad2": self.dificultades[1],
                "dificultad3": self.dificultades[2],
                "puntaje_final": self.calcular_puntaje_final(),
                "estado_participante": self.clasificar_puntaje()
            }    

class GestionarParticipantes:
    def __init__(self,archivo="participantes.csv"):
        self.archivo=archivo
        self.campos = ["id", "nombre","resultado1", "resultado2", "resultado3","dificultad1", "dificultad2", "dificultad3","puntaje_final", "estado_participante"]
        self.contador_id=self.recuperar_ultimo_id() + 1

    def añadir_participante(self, nombre,resultados):
        nuevo_participante = Participante(self.contador_id, nombre,resultados)
        
        with open(self.archivo, 'a', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=self.campos)
            if os.path.getsize(self.archivo) == 0:
                writer.writeheader()
            writer.writerow(nuevo_participante.reporte_participante())
        
        self.contador_id += 1
    
    def mostrar_participantes_id(self,id_participante):
        
        df=self.leer_csv_participantes()
        df['id'] = df['id'].astype(str)
        id = str(id_participante)
        
        return df[df["id"]==id]

    
    def leer_csv_participantes(self):
        if os.path.isfile(self.archivo):
            return pd.read_csv(self.archivo)
        return pd.DataFrame(columns=self.campos)
    
    
    def recuperar_ultimo_id(self):
        if os.path.isfile(self.archivo):
             df = self.leer_csv_participantes()
             if not df.empty:
                 return df["id"].max()
        return 0