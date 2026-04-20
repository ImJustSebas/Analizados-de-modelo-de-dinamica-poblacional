"""
Funciones para generar gráficos con Matplotlib y embeberlos en Tkinter.
"""
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def dibujar_grafico_exponencial_logistico(figura, ejes, t, poblacion, titulo):
    """Dibuja el gráfico de población vs tiempo para modelos de una especie."""
    ejes.clear()
    ejes.plot(t, poblacion, 'b-', linewidth=2)
    ejes.set_xlabel('Tiempo')
    ejes.set_ylabel('Población')
    ejes.set_title(titulo)
    ejes.grid(True, linestyle='--', alpha=0.6)
    figura.tight_layout()
    figura.canvas.draw()

def dibujar_grafico_lotka_volterra(figura, ejes, t, presas, depredadores):
    """Dibuja gráfico de poblaciones vs tiempo y plano de fase."""
    # Limpiar figura completa y crear subplots
    figura.clear()
    ax1 = figura.add_subplot(121)
    ax2 = figura.add_subplot(122)

    ax1.plot(t, presas, 'g-', label='Presas', linewidth=2)
    ax1.plot(t, depredadores, 'r-', label='Depredadores', linewidth=2)
    ax1.set_xlabel('Tiempo')
    ax1.set_ylabel('Población')
    ax1.set_title('Poblaciones vs Tiempo')
    ax1.legend()
    ax1.grid(True, linestyle='--', alpha=0.6)

    ax2.plot(presas, depredadores, 'k-', linewidth=2)
    ax2.set_xlabel('Presas')
    ax2.set_ylabel('Depredadores')
    ax2.set_title('Plano de Fase')
    ax2.grid(True, linestyle='--', alpha=0.6)

    figura.tight_layout()
    figura.canvas.draw()

def dibujar_grafico_sir(figura, ejes, t, susceptibles, infectados, recuperados):
    """Dibuja el gráfico para el modelo SIR."""
    ejes.clear()
    ejes.plot(t, susceptibles, 'b-', label='Susceptibles', linewidth=2)
    ejes.plot(t, infectados, 'r-', label='Infectados', linewidth=2)
    ejes.plot(t, recuperados, 'g-', label='Recuperados', linewidth=2)
    ejes.set_xlabel('Tiempo')
    ejes.set_ylabel('Número de individuos')
    ejes.set_title('Modelo SIR')
    ejes.legend()
    ejes.grid(True, linestyle='--', alpha=0.6)
    figura.tight_layout()
    figura.canvas.draw()

def limpiar_grafico(figura, ejes):
    """Borra el contenido del gráfico."""
    ejes.clear()
    figura.canvas.draw()