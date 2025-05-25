import tkinter as tk
from tkinter import messagebox
from tkinter import font
from logica import GestionarParticipantes
from analisis import DataAnalyzer
import pandas as pd
from PIL import ImageTk
import os

#Instanciar las clases
participantes = GestionarParticipantes()
analizar = None
if os.path.isfile("participantes.csv"):
    analizar = DataAnalyzer("participantes.csv")

#Crear ventana
base = tk.Tk()
base.title("Gestor de Participantes")
base.geometry("900x8000")
base.configure(bg="#f0f4f7")


#Volver fuentes negrilla
negrita = font.Font(weight="bold")

#Entradas
campos = [
    ("Nombre:", 0),
    ("Resultado Resistencia:", 1),
    ("Resultado Fuerza:", 2),
    ("Resultado Velocidad:", 3),
    ("Buscar por Id:", 4)
]

#Mapeo campos y devuelvo un componente tk.label
entradas = []
for campo, fila in campos:
    tk.Label(base, text=campo, font=negrita, bg="#f0f4f7").grid(row=fila, column=0, padx=10, pady=5, sticky="e")
    entrada = tk.Entry(base, width=30)
    entrada.grid(row=fila, column=1, padx=10, pady=5, sticky="w")
    entradas.append(entrada)

entry_nombre, entry_resul_resistencia, entry_resul_fuerza, entry_resul_velocidad, entry_id_participante = entradas

#Funcionalidades de botones
def agregar_participante():
    nombre = entry_nombre.get().strip()
    resultado_resistencia = entry_resul_resistencia.get()
    resultado_fuerza = entry_resul_fuerza.get()
    resultado_velocidad = entry_resul_velocidad.get()

    if not all([nombre, resultado_resistencia, resultado_fuerza, resultado_velocidad]):
        messagebox.showwarning("Campos vacíos", "Por favor completa todos los campos.")
        return
    try:
        resultados = [float(resultado_resistencia), float(resultado_fuerza), float(resultado_velocidad)]
    except ValueError:
        messagebox.showerror("Error", "Los resultados deben ser números.")
        return
    
    if not all(0 <= resultado <= 100 for resultado in resultados):
        messagebox.showerror("Error de rango", "Todos los resultados deben estar entre 0 y 100.")
        return

    participantes.añadir_participante(nombre, resultados)
    messagebox.showinfo("Éxito", "Participante registrado.")
    mostrar_participantes()
    limpiar_campos()

def mostrar_participantes():
    text_area.delete("1.0", tk.END)
    df = participantes.leer_csv_participantes()

    if not df.empty:
        encabezado = f"{'ID':<5}{'Nombre':<15}{'Resultados':<25}{'Dificultades':<30}{'Puntaje':<10}{'Estado':<15}\n"
        encabezado += "-" * 105 + "\n"
        text_area.insert(tk.END, encabezado)

        df["resultados"] = df[["resultado1", "resultado2", "resultado3"]].values.tolist()
        df["dificultades"] = df[["dificultad1", "dificultad2", "dificultad3"]].values.tolist()
        
        for _, fila in df.iterrows():
            linea = f"{str(fila['id']):<5}{fila['nombre']:<15}{str(fila['resultados']):<25}{str(fila['dificultades']):<30}{str(fila['puntaje_final']):<10}{fila['estado_participante']:<15}\n"
            text_area.insert(tk.END, linea)
        text_area.insert(tk.END,f"El promedio de participantes es:{analizar.promedio_puntaje_final()}")
    else:
        text_area.insert(tk.END, "No hay participantes registrados.")


def mostrar_participantes_id():
    text_area.delete("1.0", tk.END)

    if not entry_id_participante.get():
        messagebox.showwarning("Campos vacíos", "Por favor completa el ID.")
        return
    
    id_participante = entry_id_participante.get()
    df = participantes.mostrar_participantes_id(id_participante)

    if isinstance(df, pd.DataFrame) and not df.empty:
        encabezado = f"{'ID':<5}{'Nombre':<15}{'Puntaje':<10}{'Estado':<15}\n"
        encabezado += "-" * 50 + "\n"
        text_area.insert(tk.END, encabezado)
        for _, fila in df.iterrows():
            text_area.insert(tk.END, f"{str(fila['id']):<5}{fila['nombre']:<15}{str(fila['puntaje_final']):<10}{fila['estado_participante']:<15}\n")
    else:
        text_area.insert(tk.END, "No existe el participante con ese ID.")

def limpiar_campos():
    for entrada in entradas:
        entrada.delete(0, tk.END)

def mostrar_imagenes(pil_img):
    image_tk = ImageTk.PhotoImage(pil_img)

    for widget in image_container.winfo_children():
        widget.destroy()

    img_label = tk.Label(image_container, image=image_tk, bg="#f0f4f7")
    img_label.image = image_tk
    img_label.pack()
    image_container.update_idletasks()
    canvas.config(scrollregion=canvas.bbox("all"))

def verificar_datos():
    if analizar is None:
        messagebox.showerror("Error", "No hay datos para mostrar")
        return False
    return True

def obtener_id(id):
    if not id:
        messagebox.showwarning("Campos vacíos", "Por favor completa el ID.")
        return None
    return id

def mostrar_grafico_circular():
    
    if not verificar_datos():
        return
    img = analizar.grafico_circular()
    if img:
        mostrar_imagenes(img)
    else:
        messagebox.showerror("Error", "No existe persona con ese ID")
        
def mostrar_matriz_correlacion():
    if not verificar_datos():
        return

    img = analizar.correlation_matrix()
    mostrar_imagenes(img)

def mostrar_histograma_resultados():
    if not verificar_datos():
        return

    img = analizar.histograma_resultados()
    mostrar_imagenes(img)

def mostrar_histograma_dificultades():
    if not verificar_datos():
        return

    img = analizar.histograma_dificultades()
    mostrar_imagenes(img)

def mostrar_histograma_resultados_id():
    if not verificar_datos():
        return
    
    id_str = entry_id_participante.get()
    if not id_str.isdigit():
        messagebox.showerror("Error", "El ID debe ser un número entero.")
        return
    
    id = int(id_str)
    img = analizar.histograma_resultados_id(id)
    
    if img:
        mostrar_imagenes(img)
    else:
        messagebox.showerror("Error", "No existe persona con ese ID")

def mostrar_histograma_ponderado_por_prueba_id():
    if not verificar_datos():
        return
    
    id_str = entry_id_participante.get()
    if not id_str.isdigit():
        messagebox.showerror("Error", "El ID debe ser un número entero.")
        return

    id = int(id_str)
    img = analizar.histograma_ponderado_por_prueba_id(id)
    
    if img:
        mostrar_imagenes(img)
    else:
        messagebox.showerror("Error", "No existe persona con ese ID")

def mostrar_histograma_dificultades_id():
    if not verificar_datos():
        return

    id_str = entry_id_participante.get()
    if not id_str.isdigit():
        messagebox.showerror("Error", "El ID debe ser un número entero.")
        return

    id = int(id_str)
    img = analizar.histograma_dificultades_id(id)
    
    if img:
        mostrar_imagenes(img)
    else:
        messagebox.showerror("Error", "No existe persona con ese ID")


#Estilo sw botones
boton_estilo = {
    "width": 20,
    "padx": 5,
    "pady": 5,
    "bd": 0,
    "fg": "white",
    "font": ("Helvetica", 10, "bold"),
}

#botones - Trae todas las propiedades del diccionario boton_estilo y la coloca en cada bo´ton

padx_val = 4
pady_val = 2


tk.Button(base, text="Agregar", bg="#00C853", command=agregar_participante, **boton_estilo).grid(row=5, column=0, padx=padx_val, pady=pady_val)
tk.Button(base, text="Buscar por ID", bg="#00B8D4", command=mostrar_participantes_id, **boton_estilo).grid(row=5, column=1, padx=padx_val, pady=pady_val)
tk.Button(base, text="Gráfico Circular", bg="#FFD600", command=mostrar_grafico_circular, **boton_estilo).grid(row=5, column=2, padx=padx_val, pady=pady_val)

tk.Button(base, text="Histograma Resultados", bg="#D500F9", command=mostrar_histograma_resultados, **boton_estilo).grid(row=6, column=0, padx=padx_val, pady=pady_val)
tk.Button(base, text="Matriz Correlación", bg="#FF6D00", command=mostrar_matriz_correlacion, **boton_estilo).grid(row=6, column=1, padx=padx_val, pady=pady_val)
tk.Button(base, text="Histograma Dificultades", bg="#64DD17", command=mostrar_histograma_dificultades, **boton_estilo).grid(row=6, column=2, padx=padx_val, pady=pady_val)

tk.Button(base, text="Resultados Por persona", bg="#6200EA", command=mostrar_histograma_resultados_id, **boton_estilo).grid(row=7, column=0, padx=padx_val, pady=pady_val)
tk.Button(base, text="Ponderado Persona", bg="#AA00FF", command=mostrar_histograma_ponderado_por_prueba_id, **boton_estilo).grid(row=7, column=1, padx=padx_val, pady=pady_val)
tk.Button(base, text="Dificultades Por persona", bg="#C51162", command=mostrar_histograma_dificultades_id, **boton_estilo).grid(row=7, column=2, padx=padx_val, pady=pady_val)

#Frame del texto a mostrar info csv
frame_texto = tk.Frame(base, bg="#f0f4f7")
frame_texto.grid(row=8, column=0, columnspan=3, padx=10, pady=10, sticky="nsew")

base.grid_rowconfigure(8, weight=1)
base.grid_columnconfigure(1, weight=1)

#Text area
tk.Label(frame_texto, text="Participantes Registrados", font=("Helvetica", 12, "bold"), bg="#f0f4f7").pack(anchor="w", pady=(10, 5))
text_area = tk.Text(frame_texto, height=50, wrap=tk.WORD, bd=2, relief="groove", font=("Courier", 10))
text_area.pack(fill="both", expand=True)

# Imagen con scroll
frame_imagen = tk.Frame(base, bg="#f0f4f7")
frame_imagen.grid(row=9, column=0, columnspan=3, padx=10, pady=10, sticky="nsew")
base.grid_rowconfigure(9, weight=2)

canvas= tk.Canvas(frame_imagen, width=1000, height=1500, bg="#f0f4f7")  # aumentamos la altura
scrollbar_y = tk.Scrollbar(frame_imagen, orient="vertical", command=canvas.yview)
scrollbar_x = tk.Scrollbar(frame_imagen, orient="horizontal", command=canvas.xview)
canvas.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)

canvas.grid(row=0, column=0, sticky="nsew")
scrollbar_y.grid(row=0, column=1, sticky="ns")
scrollbar_x.grid(row=1, column=0, sticky="ew")

frame_imagen.grid_rowconfigure(0, weight=1)
frame_imagen.grid_columnconfigure(0, weight=1)

image_container = tk.Frame(canvas, bg="#f0f4f7")
canvas.create_window((0, 0), window=image_container, anchor="nw")

# Mostrar datos al iniciar
mostrar_participantes()

# Main loop
base.mainloop()
