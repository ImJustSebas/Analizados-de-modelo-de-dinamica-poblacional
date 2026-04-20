# Simulador de Dinámica Poblacional

Aplicación de escritorio desarrollada en Python para simular modelos matemáticos de dinámica de poblaciones, con interfaz gráfica intuitiva basada en Tkinter y visualización de resultados con Matplotlib.

## Características

- **Modelos implementados**:
  - Crecimiento Exponencial
  - Crecimiento Logístico
  - Modelo Presa-Depredador (Lotka-Volterra)
  - Modelo epidemiológico SIR (Susceptibles-Infectados-Recuperados)
- Interfaz gráfica construida con `tkinter.ttk`.
- Gráficos embebidos de Matplotlib actualizables.
- Validación de parámetros y mensajes de error amigables.
- Resumen estadístico de la simulación (valores máximos, mínimos, finales).

## Requisitos

- Python 3.10 o superior
- Dependencias listadas en `requirements.txt`

## Instalación

1. Clonar este repositorio o descargar los archivos fuente.
2. Crear un entorno virtual (opcional pero recomendado):
python -m venv venv
source venv/bin/activate # En Windows: venv\Scripts\activate

text
3. Instalar las dependencias:
pip install -r requirements.txt

text

## Uso

Ejecutar el programa desde la terminal:
python main.py

text

### Instrucciones de uso

1. Seleccionar el modelo deseado en el menú desplegable.
2. Ingresar los parámetros solicitados (los valores por defecto son razonables para pruebas).
3. Presionar el botón **Simular**.
4. El gráfico se mostrará en el área central y un resumen aparecerá en la parte inferior.
5. El botón **Limpiar** borra el gráfico y el área de mensajes.

### Parámetros de cada modelo

- **Crecimiento Exponencial**:
  - Población inicial, tasa de crecimiento, tiempo máximo, paso de tiempo.
- **Crecimiento Logístico**:
  - Población inicial, tasa de crecimiento, capacidad de carga (K), tiempo máximo, paso de tiempo.
- **Lotka-Volterra**:
  - Presas iniciales, depredadores iniciales, parámetros alfa, beta, delta, gamma, tiempo máximo, paso de tiempo.
- **SIR**:
  - Población total, susceptibles iniciales, infectados iniciales, recuperados iniciales, beta (transmisión), gamma (recuperación), tiempo máximo, paso de tiempo.

## Estructura del proyecto
.
├── main.py # Punto de entrada
├── modelo.py # Definición de ecuaciones diferenciales
├── simulacion.py # Lógica de simulación (solve_ivp)
├── ui.py # Interfaz gráfica (Tkinter)
├── graficos.py # Funciones de visualización con Matplotlib
├── utils.py # Validaciones y utilidades
├── requirements.txt # Dependencias
└── README.md

text

## Notas técnicas

- Se utiliza `scipy.integrate.solve_ivp` para resolver las ecuaciones diferenciales.
- Los gráficos se actualizan limpiando la figura antes de redibujar.
- La validación de entradas evita parámetros inválidos (negativos, ceros en campos críticos, etc.).
- El código sigue las convenciones de estilo PEP8 y está comentado en español.

## Autor

Desarrollado como proyecto de portafolio para demostrar habilidades en Python, modelado matemático y desarrollo de interfaces gráficas.
