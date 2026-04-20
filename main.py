"""
Punto de entrada de la aplicación Simulador de Dinámica Poblacional.
Inicializa la ventana principal y la interfaz de usuario.
"""
import tkinter as tk
from ui import InterfazSimulador

if __name__ == "__main__":
    raiz = tk.Tk()
    app = InterfazSimulador(raiz)
    raiz.mainloop()