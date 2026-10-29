"""Ejercicio 1 - Suma de dos colas elemento a elemento (con interfaz gráfica)."""
import random
import tkinter as tk
from tkinter import messagebox

from cola import Cola


# ---------------------------------------------------------------------------
# LÓGICA (la función que pide el ejercicio)
# ---------------------------------------------------------------------------
def sumar_colas(cola_a, cola_b):
    """Recibe 2 colas de enteros y devuelve una NUEVA cola con la suma uno a uno.
    Trabaja con copias para no destruir las colas originales.
    Si una cola es más corta, sus elementos faltantes se toman como 0."""
    a, b = cola_a.copiar(), cola_b.copiar()
    resultado = Cola()
    while not a.esta_vacia() or not b.esta_vacia():
        x = a.desencolar() if not a.esta_vacia() else 0
        y = b.desencolar() if not b.esta_vacia() else 0
        resultado.encolar(x + y)
    return resultado


# ---------------------------------------------------------------------------
# INTERFAZ
# ---------------------------------------------------------------------------
BG, PANEL, TXT = "#1e1e2e", "#2a2a40", "#f5f5f5"
COL_A, COL_B, COL_R = "#4cc9f0", "#f72585", "#80ed99"


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Suma de Colas")
        self.configure(bg=BG)
        self.resizable(False, False)

        self.A, self.B, self.R = Cola(), Cola(), Cola()

        tk.Label(self, text="➕ Suma de Colas", font=("Segoe UI", 20, "bold"),
                 bg=BG, fg=TXT).pack(pady=(12, 0))
        tk.Label(self, text="Cada elemento de A se suma con el de B en la misma posición",
                 bg=BG, fg="#aaa").pack()

        self.canvas = tk.Canvas(self, width=720, height=430, bg=PANEL,
                                highlightthickness=0)
        self.canvas.pack(padx=15, pady=10)

        # --- controles ---
        barra = tk.Frame(self, bg=BG)
        barra.pack(pady=4)
        self.entrada = tk.Entry(barra, width=8, font=("Segoe UI", 14), justify="center")
        self.entrada.grid(row=0, column=0, padx=6)
        self.entrada.bind("<Return>", lambda e: self.agregar("A"))
        self.boton(barra, "Encolar en A", COL_A, lambda: self.agregar("A"), 0, 1)
        self.boton(barra, "Encolar en B", COL_B, lambda: self.agregar("B"), 0, 2)

        barra2 = tk.Frame(self, bg=BG)
        barra2.pack(pady=(2, 12))
        self.boton(barra2, "Ejemplo del PDF", "#ffd166", self.ejemplo, 0, 0)
        self.boton(barra2, "Aleatorio", "#c77dff", self.aleatorio, 0, 1)
        self.boton(barra2, "Sumar todo", COL_R, self.sumar_todo, 0, 2)
        self.boton(barra2, "Paso a paso", "#90e0ef", self.paso, 0, 3)
        self.boton(barra2, "Limpiar", "#adb5bd", self.limpiar, 0, 4)

        self.dibujar()

    def boton(self, padre, texto, color, cmd, r, c):
        tk.Button(padre, text=texto, bg=color, fg="#111", relief="flat",
                  font=("Segoe UI", 10, "bold"), padx=10, pady=4,
                  command=cmd).grid(row=r, column=c, padx=4)

    # --- acciones ---
    def agregar(self, cual):
        try:
            n = int(self.entrada.get())
        except ValueError:
            messagebox.showwarning("Dato inválido", "Escribe un número entero.")
            return
        (self.A if cual == "A" else self.B).encolar(n)
        self.entrada.delete(0, tk.END)
        self.R.vaciar()
        self.dibujar()

    def ejemplo(self):
        self.limpiar()
        for n in (3, 4, 2, 8, 12):
            self.A.encolar(n)
        for n in (6, 2, 9, 11, 3):
            self.B.encolar(n)
        self.dibujar()

    def aleatorio(self):
        self.limpiar()
        for _ in range(random.randint(3, 7)):
            self.A.encolar(random.randint(1, 20))
            self.B.encolar(random.randint(1, 20))
        self.dibujar()

    def sumar_todo(self):
        """Usa la función sumar_colas (no destruye A ni B)."""
        self.R = sumar_colas(self.A, self.B)
        self.dibujar()

    def paso(self):
        """Saca el frente de A y B (como una cola real) y encola la suma en R."""
        if self.A.esta_vacia() and self.B.esta_vacia():
            return
        x = self.A.desencolar() if not self.A.esta_vacia() else 0
        y = self.B.desencolar() if not self.B.esta_vacia() else 0
        self.R.encolar(x + y)
        self.dibujar()

    def limpiar(self):
        for c in (self.A, self.B, self.R):
            c.vaciar()
        self.dibujar()

    # --- dibujo ---
    def dibujar(self):
        cv = self.canvas
        cv.delete("all")
        columnas = [("Cola A", self.A, COL_A, 20),
                    ("Cola B", self.B, COL_B, 260),
                    ("Resultado", self.R, COL_R, 500)]
        for titulo, cola, color, x in columnas:
            cv.create_text(x + 100, 22, text=titulo, fill=color,
                           font=("Segoe UI", 15, "bold"))
            cv.create_text(x + 100, 44, text="▼ frente", fill="#888",
                           font=("Segoe UI", 9))
            for i, valor in enumerate(cola.elementos()[:8]):
                y = 60 + i * 44
                relleno = color if i == 0 else PANEL
                letra = "#111" if i == 0 else TXT
                cv.create_rectangle(x + 30, y, x + 170, y + 38, fill=relleno,
                                    outline=color, width=2)
                cv.create_text(x + 100, y + 19, text=str(valor), fill=letra,
                               font=("Segoe UI", 15, "bold"))
            if cola.tamanio() > 8:
                cv.create_text(x + 100, 60 + 8 * 44 + 6,
                               text=f"... +{cola.tamanio() - 8} más", fill="#888")
        cv.create_text(230, 215, text="+", fill=TXT, font=("Segoe UI", 28, "bold"))
        cv.create_text(470, 215, text="=", fill=TXT, font=("Segoe UI", 28, "bold"))


if __name__ == "__main__":
    App().mainloop()
