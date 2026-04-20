"""
Construcción de la interfaz gráfica con Tkinter y ttk.
Maneja los eventos del usuario y la comunicación con los demás módulos.
"""
import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

import simulacion
import graficos
import utils

class InterfazSimulador:
    def __init__(self, raiz):
        self.raiz = raiz
        self.raiz.title("Simulador de Dinámica Poblacional")
        self.raiz.geometry("1000x750")
        self.raiz.resizable(True, True)

        # Variables de control
        self.modelo_var = tk.StringVar()
        self.param_entries = {}
        self.resultado_texto = None

        # Configurar figura de matplotlib
        self.figura = plt.Figure(figsize=(6, 4), dpi=100)
        self.ejes = self.figura.add_subplot(111)

        self.crear_widgets()
        self.inicializar_modelo()

    def crear_widgets(self):
        # Frame principal
        frame_principal = ttk.Frame(self.raiz, padding="10")
        frame_principal.pack(fill=tk.BOTH, expand=True)

        # Panel superior: selección de modelo
        panel_superior = ttk.LabelFrame(frame_principal, text="Configuración del Modelo", padding="10")
        panel_superior.pack(fill=tk.X, pady=(0, 10))

        ttk.Label(panel_superior, text="Modelo:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.combo_modelo = ttk.Combobox(
            panel_superior,
            textvariable=self.modelo_var,
            values=["Crecimiento Exponencial", "Crecimiento Logístico", "Lotka-Volterra", "SIR"],
            state="readonly",
            width=25
        )
        self.combo_modelo.grid(row=0, column=1, sticky=tk.W, padx=5, pady=5)
        self.combo_modelo.bind('<<ComboboxSelected>>', self.cambiar_modelo)

        # Frame para parámetros dinámicos
        self.frame_parametros = ttk.Frame(panel_superior)
        self.frame_parametros.grid(row=1, column=0, columnspan=3, sticky=tk.W, pady=10)

        # Botones de acción
        frame_botones = ttk.Frame(panel_superior)
        frame_botones.grid(row=2, column=0, columnspan=3, pady=5)

        self.boton_simular = ttk.Button(frame_botones, text="Simular", command=self.ejecutar_simulacion)
        self.boton_simular.pack(side=tk.LEFT, padx=5)

        self.boton_limpiar = ttk.Button(frame_botones, text="Limpiar", command=self.limpiar_todo)
        self.boton_limpiar.pack(side=tk.LEFT, padx=5)

        # Panel central: gráfico y resultados
        panel_central = ttk.Frame(frame_principal)
        panel_central.pack(fill=tk.BOTH, expand=True)

        # Lienzo de matplotlib
        self.canvas = FigureCanvasTkAgg(self.figura, master=panel_central)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # Área de texto para resumen / errores
        frame_resultados = ttk.LabelFrame(panel_central, text="Resultados / Mensajes", padding="5")
        frame_resultados.pack(fill=tk.X, pady=(5, 0))

        self.resultado_texto = tk.Text(frame_resultados, height=6, state=tk.DISABLED, wrap=tk.WORD)
        scroll = ttk.Scrollbar(frame_resultados, orient=tk.VERTICAL, command=self.resultado_texto.yview)
        self.resultado_texto.configure(yscrollcommand=scroll.set)
        self.resultado_texto.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scroll.pack(side=tk.RIGHT, fill=tk.Y)

    def inicializar_modelo(self):
        """Establece el modelo por defecto."""
        self.modelo_var.set("Crecimiento Exponencial")
        self.cambiar_modelo()

    def cambiar_modelo(self, event=None):
        """Actualiza los campos de entrada según el modelo seleccionado."""
        # Limpiar frame de parámetros
        for widget in self.frame_parametros.winfo_children():
            widget.destroy()

        modelo = self.modelo_var.get()
        self.param_entries.clear()

        if modelo == "Crecimiento Exponencial":
            campos = [
                ("Población inicial:", "poblacion_inicial", "100"),
                ("Tasa de crecimiento (r):", "tasa_crecimiento", "0.1"),
                ("Tiempo máximo:", "tiempo_maximo", "50"),
                ("Paso de tiempo (dt):", "paso_tiempo", "0.1")
            ]
        elif modelo == "Crecimiento Logístico":
            campos = [
                ("Población inicial:", "poblacion_inicial", "10"),
                ("Tasa de crecimiento (r):", "tasa_crecimiento", "0.2"),
                ("Capacidad de carga (K):", "capacidad_carga", "1000"),
                ("Tiempo máximo:", "tiempo_maximo", "50"),
                ("Paso de tiempo (dt):", "paso_tiempo", "0.1")
            ]
        elif modelo == "Lotka-Volterra":
            campos = [
                ("Presas iniciales:", "presas_inicial", "40"),
                ("Depredadores iniciales:", "depredadores_inicial", "9"),
                ("Alfa (tasa crecimiento presas):", "alfa", "0.1"),
                ("Beta (tasa depredación):", "beta", "0.02"),
                ("Delta (eficiencia conversión):", "delta", "0.01"),
                ("Gamma (mortalidad depredadores):", "gamma", "0.1"),
                ("Tiempo máximo:", "tiempo_maximo", "200"),
                ("Paso de tiempo (dt):", "paso_tiempo", "0.1")
            ]
        elif modelo == "SIR":
            campos = [
                ("Población total (N):", "poblacion_total", "1000"),
                ("Susceptibles iniciales:", "susceptibles_inicial", "999"),
                ("Infectados iniciales:", "infectados_inicial", "1"),
                ("Recuperados iniciales:", "recuperados_inicial", "0"),
                ("Beta (tasa de transmisión):", "beta", "0.3"),
                ("Gamma (tasa de recuperación):", "gamma", "0.1"),
                ("Tiempo máximo:", "tiempo_maximo", "100"),
                ("Paso de tiempo (dt):", "paso_tiempo", "0.1")
            ]
        else:
            return

        # Crear entradas
        for i, (label, key, default) in enumerate(campos):
            ttk.Label(self.frame_parametros, text=label).grid(row=i, column=0, sticky=tk.W, padx=5, pady=2)
            entry = ttk.Entry(self.frame_parametros, width=15)
            entry.insert(0, default)
            entry.grid(row=i, column=1, sticky=tk.W, padx=5, pady=2)
            self.param_entries[key] = entry

    def obtener_parametros(self):
        """Recupera y valida los parámetros ingresados."""
        modelo = self.modelo_var.get()
        params = {}
        errores = []

        for key, entry in self.param_entries.items():
            valor_str = entry.get().strip()
            if not valor_str:
                errores.append(f"El campo '{key}' está vacío.")
                continue
            try:
                valor = float(valor_str)
            except ValueError:
                errores.append(f"El campo '{key}' debe ser un número.")
                continue
            params[key] = valor

        if errores:
            raise ValueError("\n".join(errores))

        # Validaciones específicas
        try:
            utils.validar_parametros_comunes(params)
            if modelo == "Crecimiento Exponencial":
                utils.validar_exponencial(params)
            elif modelo == "Crecimiento Logístico":
                utils.validar_logistico(params)
            elif modelo == "Lotka-Volterra":
                utils.validar_lotka_volterra(params)
            elif modelo == "SIR":
                utils.validar_sir(params)
        except ValueError as e:
            raise ValueError(str(e))

        return params

    def ejecutar_simulacion(self):
        """Obtiene parámetros, ejecuta la simulación y muestra resultados."""
        try:
            params = self.obtener_parametros()
        except ValueError as e:
            self.mostrar_error(str(e))
            return

        modelo = self.modelo_var.get()
        try:
            resultados = simulacion.ejecutar_simulacion(modelo, params)
        except Exception as e:
            self.mostrar_error(f"Error en la simulación: {e}")
            return

        # Dibujar según el modelo
        if modelo == "Crecimiento Exponencial" or modelo == "Crecimiento Logístico":
            t, pob = resultados
            graficos.dibujar_grafico_exponencial_logistico(
                self.figura, self.ejes, t, pob, modelo
            )
            self.mostrar_resumen_univariado(t, pob, modelo)
        elif modelo == "Lotka-Volterra":
            t, presas, depredadores = resultados
            graficos.dibujar_grafico_lotka_volterra(
                self.figura, self.ejes, t, presas, depredadores
            )
            self.mostrar_resumen_lotka(t, presas, depredadores)
        elif modelo == "SIR":
            t, S, I, R = resultados
            graficos.dibujar_grafico_sir(self.figura, self.ejes, t, S, I, R)
            self.mostrar_resumen_sir(t, S, I, R)
        else:
            self.mostrar_error("Modelo no implementado.")

    def mostrar_error(self, mensaje):
        """Muestra un mensaje de error en el área de texto."""
        self.resultado_texto.config(state=tk.NORMAL)
        self.resultado_texto.delete(1.0, tk.END)
        self.resultado_texto.insert(tk.END, f"ERROR: {mensaje}")
        self.resultado_texto.config(state=tk.DISABLED)
        messagebox.showerror("Error de validación", mensaje)

    def mostrar_resumen_univariado(self, t, poblacion, titulo):
        """Muestra estadísticas para modelos de una sola población."""
        maximo = np.max(poblacion)
        minimo = np.min(poblacion)
        final = poblacion[-1]
        texto = (
            f"Modelo: {titulo}\n"
            f"Población máxima: {maximo:.2f}\n"
            f"Población mínima: {minimo:.2f}\n"
            f"Población final (t={t[-1]:.2f}): {final:.2f}"
        )
        self.actualizar_texto_resultado(texto)

    def mostrar_resumen_lotka(self, t, presas, depredadores):
        """Muestra resumen para Lotka-Volterra."""
        max_presas = np.max(presas)
        min_presas = np.min(presas)
        max_dep = np.max(depredadores)
        min_dep = np.min(depredadores)
        final_presas = presas[-1]
        final_dep = depredadores[-1]
        texto = (
            f"Modelo: Lotka-Volterra\n"
            f"Presas - Máx: {max_presas:.2f}, Mín: {min_presas:.2f}, Final: {final_presas:.2f}\n"
            f"Depredadores - Máx: {max_dep:.2f}, Mín: {min_dep:.2f}, Final: {final_dep:.2f}"
        )
        self.actualizar_texto_resultado(texto)

    def mostrar_resumen_sir(self, t, S, I, R):
        """Muestra resumen para SIR."""
        max_I = np.max(I)
        t_pico = t[np.argmax(I)]
        final_S = S[-1]
        final_I = I[-1]
        final_R = R[-1]
        texto = (
            f"Modelo: SIR\n"
            f"Pico de infectados: {max_I:.2f} en t={t_pico:.2f}\n"
            f"Final - Susceptibles: {final_S:.2f}, Infectados: {final_I:.2f}, Recuperados: {final_R:.2f}"
        )
        self.actualizar_texto_resultado(texto)

    def actualizar_texto_resultado(self, texto):
        """Escribe texto en el área de resultados."""
        self.resultado_texto.config(state=tk.NORMAL)
        self.resultado_texto.delete(1.0, tk.END)
        self.resultado_texto.insert(tk.END, texto)
        self.resultado_texto.config(state=tk.DISABLED)

    def limpiar_todo(self):
        """Limpia el gráfico y el área de resultados."""
        graficos.limpiar_grafico(self.figura, self.ejes)
        self.resultado_texto.config(state=tk.NORMAL)
        self.resultado_texto.delete(1.0, tk.END)
        self.resultado_texto.config(state=tk.DISABLED)