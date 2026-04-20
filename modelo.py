"""
Define las ecuaciones diferenciales para cada modelo poblacional.
Cada función retorna la derivada en el formato requerido por solve_ivp.
"""

def crecimiento_exponencial(t, y, tasa_crecimiento):
    """Ecuación dP/dt = r * P"""
    P = y[0]
    return [tasa_crecimiento * P]

def crecimiento_logistico(t, y, tasa_crecimiento, capacidad_carga):
    """Ecuación dP/dt = r * P * (1 - P/K)"""
    P = y[0]
    return [tasa_crecimiento * P * (1 - P / capacidad_carga)]

def lotka_volterra(t, y, alfa, beta, delta, gamma):
    """
    Modelo presa-depredador.
    y[0] = presas, y[1] = depredadores
    dx/dt = alfa*x - beta*x*y
    dy/dt = delta*x*y - gamma*y
    """
    x, y_p = y
    dxdt = alfa * x - beta * x * y_p
    dydt = delta * x * y_p - gamma * y_p
    return [dxdt, dydt]

def sir(t, y, beta, gamma, N):
    """
    Modelo epidemiológico SIR.
    y[0] = susceptibles, y[1] = infectados, y[2] = recuperados
    dS/dt = -beta * S * I / N
    dI/dt = beta * S * I / N - gamma * I
    dR/dt = gamma * I
    """
    S, I, R = y
    dSdt = -beta * S * I / N
    dIdt = beta * S * I / N - gamma * I
    dRdt = gamma * I
    return [dSdt, dIdt, dRdt]