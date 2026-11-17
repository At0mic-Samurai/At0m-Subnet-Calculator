"""At0mSubnet - calculadora de subredes IPv4 con interfaz dark neón (tkinter)."""

import ipaddress
import math
import tkinter as tk

# ---------- Tema ----------
BG = "#0a0a0f"
PANEL = "#12121a"
NEON = "#00ff15"
NEON_HOVER = "#7dff8a"
CYAN = "#00e5ff"
ERROR = "#ff3860"
DIM = "#4a5a4f"
MAGENTA = "#ff2bd6"
ACERO = "#cfd8dc"
FUENTE = "Consolas"
NOMBRE_APP = "At0mSubnet"

CAMPOS = [
    "Network ID",
    "Máscara",
    "Máscara (binario)",
    "Wildcard",
    "Broadcast",
    "Rango utilizable",
    "Hosts utilizables",
    "Tipo de IP",
    "Clase",
]

# (primer octeto mínimo, máximo, clase, descripción)
CLASES = [
    (0, 127, "A", ""),
    (128, 191, "B", ""),
    (192, 223, "C", ""),
    (224, 239, "D", " (multicast)"),
    (240, 255, "E", " (reservada)"),
]


# ---------- Lógica (independiente de la interfaz) ----------
class ErrorEntrada(ValueError):
    """Error de validación; `campo` indica qué entrada corregir ('ip' o 'cidr')."""

    def __init__(self, mensaje, campo):
        super().__init__(mensaje)
        self.campo = campo


def calcular_subred(ip_texto, cidr_texto):
    """Valida los datos y devuelve una lista de (etiqueta, valor)."""
    ip_texto = ip_texto.strip()
    cidr_texto = cidr_texto.strip().lstrip("/")

    if not ip_texto:
        raise ErrorEntrada("Ingresa una dirección IP.", "ip")
    try:
        ip = ipaddress.IPv4Address(ip_texto)
    except ValueError:
        raise ErrorEntrada(f"'{ip_texto}' no es una IPv4 válida (ej. 192.168.1.10).", "ip") from None

    if not cidr_texto:
        raise ErrorEntrada("Ingresa la máscara en notación CIDR.", "cidr")
    if not (cidr_texto.isascii() and cidr_texto.isdigit()):
        raise ErrorEntrada("El CIDR debe ser un número entero (ej. 24).", "cidr")
    cidr = int(cidr_texto)
    if not 0 <= cidr <= 32:
        raise ErrorEntrada("El CIDR debe estar entre 0 y 32.", "cidr")

    red = ipaddress.IPv4Network(f"{ip}/{cidr}", strict=False)

    # /32 = un solo host, /31 = enlace punto a punto (RFC 3021), resto = restar red y broadcast
    if cidr == 32:
        hosts, primero, ultimo, broadcast = 1, red[0], red[0], "N/A"
    elif cidr == 31:
        hosts, primero, ultimo, broadcast = 2, red[0], red[-1], "N/A"
    else:
        hosts, primero, ultimo, broadcast = red.num_addresses - 2, red[1], red[-2], red.broadcast_address

    if ip.is_unspecified:
        tipo = "No especificada (0.0.0.0)"
    elif ip.is_loopback:
        tipo = "Loopback"
    elif ip.is_link_local:
        tipo = "Link-local (APIPA)"
    elif ip.is_multicast:
        tipo = "Multicast"
    elif ip.is_reserved:
        tipo = "Reservada"
    elif ip.is_private:
        tipo = "Privada"
    else:
        tipo = "Pública"

    primer_octeto = ip.packed[0]
    for minimo, maximo, letra, nota in CLASES:
        if minimo <= primer_octeto <= maximo:
            clase = f"{letra}{nota}"
            break

    binario = ".".join(f"{octeto:08b}" for octeto in red.netmask.packed)

    return [
        ("Network ID", f"{red.network_address}/{cidr}"),
        ("Máscara", str(red.netmask)),
        ("Máscara (binario)", binario),
        ("Wildcard", str(red.hostmask)),
        ("Broadcast", str(broadcast)),
        ("Rango utilizable", f"{primero} - {ultimo}"),
        ("Hosts utilizables", f"{hosts:,}"),
        ("Tipo de IP", tipo),
        ("Clase", clase),
    ]


# ---------- Ícono (átomo + katanas, dibujado con el Canvas) ----------
def _rotar(puntos, grados, cx, cy):
    """Rota una lista de (x, y) alrededor de (cx, cy) y la devuelve aplanada."""
    a = math.radians(grados)
    c, s = math.cos(a), math.sin(a)
    plano = []
    for x, y in puntos:
        dx, dy = x - cx, y - cy
        plano += [cx + dx * c - dy * s, cy + dx * s + dy * c]
    return plano


def _elipse(cx, cy, a, b, grados, pasos=48):
    """Puntos de una elipse de semiejes a, b rotada `grados`."""
    puntos = [(cx + a * math.cos(2 * math.pi * i / pasos),
               cy + b * math.sin(2 * math.pi * i / pasos)) for i in range(pasos)]
    return _rotar(puntos, grados, cx, cy)


def dibujar_icono(canvas, tam=72):
    """Dibuja un átomo neón con dos katanas cruzadas detrás."""
    cx = cy = tam / 2
    k = tam / 72  # factor de escala

    # Katanas (hoja hacia arriba, guarda y empuñadura hacia abajo), rotadas ±45°
    hoja = [(cx - 2.2 * k, cy + 12 * k), (cx - 2.2 * k, cy - 30 * k),
            (cx + 2.4 * k, cy - 36 * k), (cx + 2.4 * k, cy + 12 * k)]
    guarda = [(cx - 6 * k, cy + 12 * k), (cx + 6 * k, cy + 12 * k),
              (cx + 6 * k, cy + 15 * k), (cx - 6 * k, cy + 15 * k)]
    mango = [(cx - 2.5 * k, cy + 15 * k), (cx + 2.5 * k, cy + 15 * k),
             (cx + 2.5 * k, cy + 32 * k), (cx - 2.5 * k, cy + 32 * k)]
    for angulo in (45, -45):
        canvas.create_polygon(_rotar(mango, angulo, cx, cy), fill=DIM, outline=ACERO)
        canvas.create_polygon(_rotar(hoja, angulo, cx, cy), fill=CYAN, outline=ACERO)
        canvas.create_polygon(_rotar(guarda, angulo, cx, cy), fill=MAGENTA, outline=MAGENTA)

    # Órbitas del átomo
    for angulo in (0, 60, 120):
        canvas.create_polygon(_elipse(cx, cy, 27 * k, 9 * k, angulo), fill="",
                              outline=NEON, width=2, smooth=True)

    # Electrones y núcleo
    for angulo, t in ((0, 0.9), (60, 2.4), (120, 4.2)):
        px, py = cx + 27 * k * math.cos(t), cy + 9 * k * math.sin(t)
        ex, ey = _rotar([(px, py)], angulo, cx, cy)
        canvas.create_oval(ex - 3 * k, ey - 3 * k, ex + 3 * k, ey + 3 * k,
                           fill=NEON_HOVER, outline=NEON)
    canvas.create_oval(cx - 5 * k, cy - 5 * k, cx + 5 * k, cy + 5 * k,
                       fill=NEON, outline=NEON_HOVER, width=2)


# ---------- Interfaz ----------
class SubnetCalculatorApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title(NOMBRE_APP)
        self.configure(bg=BG)
        self.resizable(False, False)

        self.resultados = []
        self.valores = {campo: tk.StringVar(value="—") for campo in CAMPOS}

        self._construir_interfaz()

        # Tamaño fijo: se calcula una vez con todo construido y ya no cambia
        self.update_idletasks()
        self.geometry(f"{self.winfo_reqwidth()}x{self.winfo_reqheight()}")
        self.pack_propagate(False)

        self.bind("<Return>", lambda _e: self.calcular())
        self.bind("<Escape>", lambda _e: self.limpiar())
        self.entrada_ip.focus_set()

    # --- construcción ---
    def _construir_interfaz(self):
        encabezado = tk.Frame(self, bg=BG)
        encabezado.pack(pady=(18, 2))
        icono = tk.Canvas(encabezado, width=72, height=72, bg=BG, highlightthickness=0)
        icono.pack(side="left", padx=(0, 12))
        dibujar_icono(icono, 72)
        tk.Label(
            encabezado, text=f"> {NOMBRE_APP}", fg=NEON, bg=BG,
            font=(FUENTE, 22, "bold"),
        ).pack(side="left")
        tk.Label(
            self, text="IPv4 // by At0mic-Samurai · Enter = calcular · Esc = limpiar",
            fg=DIM, bg=BG, font=(FUENTE, 9),
        ).pack(pady=(0, 12))

        # Formulario
        formulario = tk.Frame(self, bg=BG)
        formulario.pack(padx=30)

        tk.Label(formulario, text="IP:", fg=CYAN, bg=BG, font=(FUENTE, 12, "bold")).grid(
            row=0, column=0, sticky="w", pady=6)
        self.entrada_ip = self._crear_entrada(formulario, ancho=22)
        self.entrada_ip.grid(row=0, column=1, padx=(10, 0), pady=6)

        tk.Label(formulario, text="CIDR: /", fg=CYAN, bg=BG, font=(FUENTE, 12, "bold")).grid(
            row=1, column=0, sticky="w", pady=6)
        validar = (self.register(self._cidr_permitido), "%P")
        self.entrada_cidr = self._crear_entrada(
            formulario, ancho=6, validate="key", validatecommand=validar)
        self.entrada_cidr.grid(row=1, column=1, padx=(10, 0), pady=6, sticky="w")

        # Botones
        botones = tk.Frame(self, bg=BG)
        botones.pack(pady=15)
        self._crear_boton(botones, "CALCULAR", self.calcular, NEON, BG, NEON_HOVER).pack(
            side="left", padx=5)
        self._crear_boton(botones, "LIMPIAR", self.limpiar, PANEL, CYAN, "#1d1d2b").pack(
            side="left", padx=5)
        self._crear_boton(botones, "COPIAR", self.copiar, PANEL, CYAN, "#1d1d2b").pack(
            side="left", padx=5)

        # Estado
        # height=2 reserva espacio para mensajes largos, así la ventana nunca cambia de alto
        self.estado = tk.Label(self, text="> Listo", fg=DIM, bg=BG, font=(FUENTE, 10),
                               wraplength=560, justify="left", anchor="nw", height=2)
        self.estado.pack(padx=30, fill="x")

        # Resultados
        panel = tk.Frame(self, bg=PANEL, highlightthickness=1, highlightbackground=DIM)
        panel.pack(padx=30, pady=(10, 25), fill="x")
        for fila, campo in enumerate(CAMPOS):
            tk.Label(panel, text=f"{campo}:", fg=CYAN, bg=PANEL, font=(FUENTE, 11),
                     anchor="w", width=19).grid(row=fila, column=0, sticky="w", padx=(12, 4), pady=4)
            tk.Label(panel, textvariable=self.valores[campo], fg=NEON, bg=PANEL,
                     font=(FUENTE, 11, "bold"), anchor="w", width=40).grid(
                row=fila, column=1, sticky="w", padx=(0, 12), pady=3)

    def _crear_entrada(self, padre, ancho, **opciones):
        return tk.Entry(
            padre, width=ancho, bg=PANEL, fg=NEON, insertbackground=NEON,
            font=(FUENTE, 12), relief="flat",
            highlightthickness=1, highlightbackground=DIM, highlightcolor=NEON,
            **opciones,
        )

    def _crear_boton(self, padre, texto, comando, fondo, color_texto, fondo_hover):
        boton = tk.Button(
            padre, text=texto, command=comando, bg=fondo, fg=color_texto,
            activebackground=fondo_hover, activeforeground=color_texto,
            font=(FUENTE, 11, "bold"), relief="flat", bd=0, padx=14, pady=6,
            cursor="hand2",
        )
        boton.bind("<Enter>", lambda _e: boton.config(bg=fondo_hover))
        boton.bind("<Leave>", lambda _e: boton.config(bg=fondo))
        return boton

    # --- utilidades ---
    @staticmethod
    def _cidr_permitido(texto):
        """Solo deja escribir hasta 2 dígitos en el campo CIDR."""
        return texto == "" or (texto.isascii() and texto.isdigit() and len(texto) <= 2)

    def _mostrar_estado(self, mensaje, color):
        self.estado.config(text=mensaje, fg=color)

    def _vaciar_resultados(self):
        self.resultados = []
        for variable in self.valores.values():
            variable.set("—")

    # --- acciones ---
    def calcular(self):
        try:
            self.resultados = calcular_subred(self.entrada_ip.get(), self.entrada_cidr.get())
        except ErrorEntrada as error:
            self._vaciar_resultados()
            self._mostrar_estado(f"[ERROR] {error}", ERROR)
            campo = self.entrada_ip if error.campo == "ip" else self.entrada_cidr
            campo.focus_set()
            campo.select_range(0, tk.END)
            return

        for etiqueta, valor in self.resultados:
            self.valores[etiqueta].set(valor)
        self._mostrar_estado("[OK] Cálculo completado", NEON)

    def limpiar(self):
        self.entrada_ip.delete(0, tk.END)
        self.entrada_cidr.delete(0, tk.END)
        self._vaciar_resultados()
        self._mostrar_estado("> Listo", DIM)
        self.entrada_ip.focus_set()

    def copiar(self):
        if not self.resultados:
            self._mostrar_estado("[!] Aún no hay resultados para copiar", ERROR)
            return
        texto = "\n".join(f"{etiqueta}: {valor}" for etiqueta, valor in self.resultados)
        self.clipboard_clear()
        self.clipboard_append(texto)
        self._mostrar_estado("[OK] Resultados copiados al portapapeles", CYAN)


if __name__ == "__main__":
    SubnetCalculatorApp().mainloop()
