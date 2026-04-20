"""
Ejecuta las simulaciones utilizando scipy.integrate.solve_ivp.
Recibe los parámetros y retorna los resultados (tiempo y poblaciones).
"""
import numpy as np
from scipy.integrate import solve_ivp
import modelo

def simular_exponencial(params):
    """Simula el modelo de crecimiento exponencial."""
    t_span = (0, params['tiempo_maximo'])
    t_eval = np.arange(0, params['tiempo_maximo'] + params['paso_tiempo'], params['paso_tiempo'])
    y0 = [params['poblacion_inicial']]
    sol = solve_ivp(
        modelo.crecimiento_exponencial,
        t_span,
        y0,
        t_eval=t_eval,
        args=(params['tasa_crecimiento'],)
    )
    return sol.t, sol.y[0]

def simular_logistico(params):
    """Simula el modelo de crecimiento logístico."""
    t_span = (0, params['tiempo_maximo'])
    t_eval = np.arange(0, params['tiempo_maximo'] + params['paso_tiempo'], params['paso_tiempo'])
    y0 = [params['poblacion_inicial']]
    sol = solve_ivp(
        modelo.crecimiento_logistico,
        t_span,
        y0,
        t_eval=t_eval,
        args=(params['tasa_crecimiento'], params['capacidad_carga'])
    )
    return sol.t, sol.y[0]

def simular_lotka_volterra(params):
    """Simula el modelo Lotka-Volterra."""
    t_span = (0, params['tiempo_maximo'])
    t_eval = np.arange(0, params['tiempo_maximo'] + params['paso_tiempo'], params['paso_tiempo'])
    y0 = [params['presas_inicial'], params['depredadores_inicial']]
    sol = solve_ivp(
        modelo.lotka_volterra,
        t_span,
        y0,
        t_eval=t_eval,
        args=(params['alfa'], params['beta'], params['delta'], params['gamma'])
    )
    return sol.t, sol.y[0], sol.y[1]

def simular_sir(params):
    """Simula el modelo SIR."""
    t_span = (0, params['tiempo_maximo'])
    t_eval = np.arange(0, params['tiempo_maximo'] + params['paso_tiempo'], params['paso_tiempo'])
    N = params['poblacion_total']
    y0 = [params['susceptibles_inicial'], params['infectados_inicial'], params['recuperados_inicial']]
    sol = solve_ivp(
        modelo.sir,
        t_span,
        y0,
        t_eval=t_eval,
        args=(params['beta'], params['gamma'], N)
    )
    return sol.t, sol.y[0], sol.y[1], sol.y[2]

def ejecutar_simulacion(modelo_seleccionado, parametros):
    """
    Función despachadora que invoca la simulación correspondiente.
    Retorna una tupla con los resultados según el modelo.
    """
    if modelo_seleccionado == "Crecimiento Exponencial":
        return simular_exponencial(parametros)
    elif modelo_seleccionado == "Crecimiento Logístico":
        return simular_logistico(parametros)
    elif modelo_seleccionado == "Lotka-Volterra":
        return simular_lotka_volterra(parametros)
    elif modelo_seleccionado == "SIR":
        return simular_sir(parametros)
    else:
        raise ValueError("Modelo no reconocido")