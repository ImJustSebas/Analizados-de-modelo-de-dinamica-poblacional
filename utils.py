"""
Funciones auxiliares para validación de entradas y conversiones.
"""

def validar_positivo(valor, nombre):
    """Lanza ValueError si valor <= 0."""
    if valor <= 0:
        raise ValueError(f"{nombre} debe ser mayor que cero.")

def validar_no_negativo(valor, nombre):
    """Lanza ValueError si valor < 0."""
    if valor < 0:
        raise ValueError(f"{nombre} no puede ser negativo.")

def validar_parametros_comunes(params):
    """Validaciones comunes a todos los modelos."""
    validar_positivo(params.get('tiempo_maximo', 1), "Tiempo máximo")
    validar_positivo(params.get('paso_tiempo', 0.1), "Paso de tiempo")
    if params['paso_tiempo'] >= params['tiempo_maximo']:
        raise ValueError("El paso de tiempo debe ser menor que el tiempo máximo.")

def validar_exponencial(params):
    validar_no_negativo(params['poblacion_inicial'], "Población inicial")
    # tasa puede ser negativa, no se valida

def validar_logistico(params):
    validar_no_negativo(params['poblacion_inicial'], "Población inicial")
    validar_positivo(params['capacidad_carga'], "Capacidad de carga")
    if params['poblacion_inicial'] > params['capacidad_carga']:
        raise ValueError("La población inicial no puede exceder la capacidad de carga.")

def validar_lotka_volterra(params):
    validar_no_negativo(params['presas_inicial'], "Presas iniciales")
    validar_no_negativo(params['depredadores_inicial'], "Depredadores iniciales")
    validar_positivo(params['alfa'], "Alfa")
    validar_positivo(params['beta'], "Beta")
    validar_positivo(params['delta'], "Delta")
    validar_positivo(params['gamma'], "Gamma")

def validar_sir(params):
    N = params['poblacion_total']
    S0 = params['susceptibles_inicial']
    I0 = params['infectados_inicial']
    R0 = params['recuperados_inicial']
    validar_positivo(N, "Población total")
    validar_no_negativo(S0, "Susceptibles iniciales")
    validar_no_negativo(I0, "Infectados iniciales")
    validar_no_negativo(R0, "Recuperados iniciales")
    if abs((S0 + I0 + R0) - N) > 1e-6:
        raise ValueError("La suma de susceptibles, infectados y recuperados debe igualar la población total.")
    validar_positivo(params['beta'], "Beta")
    validar_positivo(params['gamma'], "Gamma")