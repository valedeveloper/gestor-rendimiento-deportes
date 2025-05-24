import tkinter as tk
from tkinter import messagebox
from tkinter import font
from logica import GestionarParticipantes
import pandas as pd

participantes = GestionarParticipantes()

# Ventana Principal
base = tk.Tk()
base.title("Gestor de Participantes")
base.geometry("900x650")
base.configure(bg="#f0f4f7")
base.resizable(False, False)

# Fuente en negrita para etiquetas
negrita = font.Font(weight="bold")

# Inputs
campos = [
    ("Nombre:", 0),
    ("Resultado Resistencia:", 1),
    ("Resultado Fuerza:", 2),
    ("Resultado Velocidad:", 3),
    ("Buscar por Id:", 4)
]

entradas = []
for texto, fila in campos:
    tk.Label(base, text=texto, font=negrita, bg="#f0f4f7").grid(row=fila, column=0, padx=10, pady=5, sticky="e")
    entrada = tk.Entry(base, width=30)
    entrada.grid(row=fila, column=1, padx=10, pady=5, sticky="w")
    entradas.append(entrada)

entry_nombre, entry_resul_resistencia, entry_resul_fuerza, entry_resul_velocidad, entry_id_participante = entradas

# Text area
tk.Label(base, text="Participantes Registrados", font=("Helvetica", 12, "bold"), bg="#f0f4f7").grid(row=5, column=0, columnspan=4, pady=(20, 5))
text_area = tk.Text(base, height=18, width=110, wrap=tk.WORD, bd=2, relief="groove", font=("Courier", 9))
text_area.grid(row=6, column=0, columnspan=6, padx=20, pady=10)


# ----- FUNCIONES -----
def agregar_participante():
    nombre = entry_nombre.get().strip()
    resultado_resistencia = entry_resul_resistencia.get()
    resultado_fuerza = entry_resul_fuerza.get()
    resultado_velocidad = entry_resul_velocidad.get()

    if not all([nombre, resultado_resistencia, resultado_fuerza, resultado_velocidad]):
        messagebox.showwarning("Campos vacíos", "Por favor completa todos los campos.")
        return

    resultados = [resultado_resistencia, resultado_fuerza, resultado_velocidad]
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
        for _, fila in df.iterrows():
            linea = f"{str(fila['id']):<5}{fila['nombre']:<15}{str(fila['resultados']):<25}{str(fila['dificultades']):<30}{str(fila['puntaje_final']):<10}{fila['estado_participante']:<15}\n"
            text_area.insert(tk.END, linea)
    else:
        text_area.insert(tk.END, "No hay participantes registrados.")

def mostrar_participantes_id():
    text_area.delete("1.0", tk.END)
    id_participante = entry_id_participante.get()
    if not id_participante:
        messagebox.showwarning("Campos vacíos", "Por favor completa el ID.")
        return

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

# Estilos botnoes
boton_estilo = {
    "width": 25,
    "padx": 5,
    "pady": 5,
    "bd": 0,
    "fg": "white",
    "font": ("Helvetica", 10, "bold"),
}

tk.Button(base, text="Agregar", bg="#28a745", command=agregar_participante, **boton_estilo).grid(row=7, column=0, columnspan=1, pady=10)
tk.Button(base, text="Mostrar Todos", bg="#007bff", command=mostrar_participantes, **boton_estilo).grid(row=7, column=1, columnspan=2, pady=10)
tk.Button(base, text="Buscar por ID", bg="#17a2b8", command=mostrar_participantes_id, **boton_estilo).grid(row=7, column=5, columnspan=1, pady=10)

# Mostrar datos al iniciar
mostrar_participantes()

# Ejecutar app
base.mainloop()
