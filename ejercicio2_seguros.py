"""Ejercicio 2 - Turnero para una compañía de seguros (con interfaz gráfica).

Comandos por consola integrada:
    C<n>  -> llega un cliente al servicio n     (ej. C1)
    A<n>  -> se atiende al siguiente del servicio n (ej. A1)
"""
import re
import tkinter as tk
from datetime import datetime

from cola import Cola

# número de servicio -> (nombre, letra del ticket, color)
SERVICIOS = {
    1: ("Siniestros",         "S", "#ef476f"),
    2: ("Pólizas nuevas",     "P", "#06d6a0"),
    3: ("Pagos",              "G", "#4cc9f0"),
    4: ("Cancelaciones",      "C", "#ffd166"),
}
BG, PANEL, TXT = "#1e1e2e", "#2a2a40", "#f5f5f5"


class Turnero(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Turnero - Seguros Yucatán")
        self.configure(bg=BG)
        self.geometry("980x640")

        # Una Cola por servicio + un contador del último número entregado
        self.colas = {n: Cola() for n in SERVICIOS}
        self.contador = {n: 0 for n in SERVICIOS}
        self.lbl_cola = {}
        self.lbl_cant = {}

        tk.Label(self, text="🛡️ Seguros Yucatán · Sistema de Turnos",
                 font=("Segoe UI", 20, "bold"), bg=BG, fg=TXT).pack(pady=(10, 4))

        cuerpo = tk.Frame(self, bg=BG)
        cuerpo.pack(fill="both", expand=True, padx=12)

        # ---------- izquierda: tarjetas de servicio ----------
        izq = tk.Frame(cuerpo, bg=BG)
        izq.pack(side="left", fill="both", expand=True)
        for n, (nombre, letra, color) in SERVICIOS.items():
            self.crear_tarjeta(izq, n, nombre, letra, color)

        # ---------- derecha: pantalla de llamado + historial ----------
        der = tk.Frame(cuerpo, bg=PANEL, width=330)
        der.pack(side="right", fill="y", padx=(10, 0))
        der.pack_propagate(False)
        tk.Label(der, text="LLAMANDO A", bg=PANEL, fg="#aaa",
                 font=("Segoe UI", 12, "bold")).pack(pady=(14, 0))
        self.lbl_llamado = tk.Label(der, text="---", bg=PANEL, fg=TXT,
                                    font=("Segoe UI", 46, "bold"))
        self.lbl_llamado.pack()
        self.lbl_detalle = tk.Label(der, text="Esperando...", bg=PANEL, fg="#aaa",
                                    font=("Segoe UI", 11))
        self.lbl_detalle.pack()
        tk.Label(der, text="Historial", bg=PANEL, fg=TXT,
                 font=("Segoe UI", 12, "bold")).pack(pady=(14, 2))
        self.log = tk.Text(der, bg="#15152a", fg=TXT, height=14, relief="flat",
                           font=("Consolas", 10), state="disabled")
        self.log.pack(fill="both", expand=True, padx=8, pady=(0, 8))

        # ---------- abajo: consola de comandos ----------
        pie = tk.Frame(self, bg=BG)
        pie.pack(fill="x", padx=12, pady=10)
        tk.Label(pie, text="Comando (C1, A1...):", bg=BG, fg=TXT,
                 font=("Segoe UI", 11)).pack(side="left")
        self.entrada = tk.Entry(pie, font=("Consolas", 14), width=10)
        self.entrada.pack(side="left", padx=8)
        self.entrada.bind("<Return>", lambda e: self.ejecutar_comando())
        self.entrada.focus()
        tk.Button(pie, text="Enviar", command=self.ejecutar_comando,
                  bg="#c77dff", relief="flat", font=("Segoe UI", 10, "bold"),
                  padx=12).pack(side="left")
        self.lbl_msg = tk.Label(pie, text="", bg=BG, fg="#ffd166",
                                font=("Segoe UI", 11))
        self.lbl_msg.pack(side="left", padx=14)

    # ---------- construcción de una tarjeta ----------
    def crear_tarjeta(self, padre, n, nombre, letra, color):
        f = tk.Frame(padre, bg=PANEL, highlightbackground=color, highlightthickness=2)
        f.pack(fill="x", pady=5)
        cab = tk.Frame(f, bg=color)
        cab.pack(fill="x")
        tk.Label(cab, text=f"  {n} · {nombre}", bg=color, fg="#111",
                 font=("Segoe UI", 13, "bold")).pack(side="left", pady=3)
        self.lbl_cant[n] = tk.Label(cab, text="0 en espera", bg=color, fg="#111",
                                    font=("Segoe UI", 10, "bold"))
        self.lbl_cant[n].pack(side="right", padx=8)

        fila = tk.Frame(f, bg=PANEL)
        fila.pack(fill="x", padx=8, pady=6)
        self.lbl_cola[n] = tk.Label(fila, text="(vacía)", bg=PANEL, fg=TXT,
                                    font=("Consolas", 12), anchor="w")
        self.lbl_cola[n].pack(side="left", fill="x", expand=True)
        tk.Button(fila, text="Llega cliente", bg=color, relief="flat",
                  command=lambda: self.llega_cliente(n)).pack(side="right", padx=3)
        tk.Button(fila, text="Atender", bg="#dddddd", relief="flat",
                  command=lambda: self.atender(n)).pack(side="right", padx=3)

    # ---------- lógica ----------
    def ticket(self, n, numero):
        return f"{SERVICIOS[n][1]}-{numero:03d}"      # ej. S-001

    def llega_cliente(self, n):
        self.contador[n] += 1
        numero = self.contador[n]
        self.colas[n].encolar(numero)
        t = self.ticket(n, numero)
        self.mensaje(f"Cliente recibe el turno {t} ({SERVICIOS[n][0]})")
        self.escribir_log(f"+ llegó   {t}")
        self.actualizar()

    def atender(self, n):
        if self.colas[n].esta_vacia():
            self.mensaje(f"No hay clientes en espera en «{SERVICIOS[n][0]}»")
            return
        numero = self.colas[n].desencolar()
        t = self.ticket(n, numero)
        self.lbl_llamado.config(text=t, fg=SERVICIOS[n][2])
        self.lbl_detalle.config(text=f"Pase a {SERVICIOS[n][0]}")
        self.mensaje(f"Llamando al turno {t}")
        self.escribir_log(f"→ llamado {t}")
        self.actualizar()

    def ejecutar_comando(self):
        texto = self.entrada.get().strip().upper()
        self.entrada.delete(0, tk.END)
        m = re.fullmatch(r"([CA])\s*(\d+)", texto)
        if not m:
            self.mensaje("Comando inválido. Usa C1, A2...")
            return
        accion, n = m.group(1), int(m.group(2))
        if n not in SERVICIOS:
            self.mensaje(f"El servicio {n} no existe (1 a {len(SERVICIOS)})")
            return
        self.llega_cliente(n) if accion == "C" else self.atender(n)

    # ---------- vista ----------
    def actualizar(self):
        for n in SERVICIOS:
            cola = self.colas[n]
            tickets = [self.ticket(n, x) for x in cola.elementos()]
            self.lbl_cant[n].config(text=f"{cola.tamanio()} en espera")
            texto = "  ".join(tickets[:6]) + (" …" if len(tickets) > 6 else "")
            self.lbl_cola[n].config(text=texto or "(vacía)")

    def mensaje(self, texto):
        self.lbl_msg.config(text=texto)

    def escribir_log(self, linea):
        hora = datetime.now().strftime("%H:%M:%S")
        self.log.config(state="normal")
        self.log.insert("1.0", f"{hora}  {linea}\n")
        self.log.config(state="disabled")


if __name__ == "__main__":
    Turnero().mainloop()
