import random
import numpy as np
from scipy.stats import norm, uniform
import matplotlib.pyplot as plt

def generar_datos(distribucion, parametros, n_muestras):
    if distribucion == 'uniforme':
        return uniform.rvs(*parametros, size=n_muestras)
    elif distribucion == 'normal':
        return norm.rvs(*parametros, size=n_muestras)

def curva_familia(x, a, b, c):
    return a * np.exp(b * x) + c

# Definición de parámetros para las distribuciones
distribuciones = {
    'resistencias': ('uniforme', (1, 10)),
    'temperaturas_agua': ('normal', (10, 5)),
    'temperaturas_ambiente': ('uniforme', (-20, 50)),
    'tensiones_alimentacion_1': ('normal', (12, 4)),
    'tensiones_alimentacion_2': ('normal', (220, 40)),
}

n_muestras = 5
x = np.linspace(0, 10, 100)

# Generación de datos y graficación
plt.figure(figsize=(10, 8))
subplot_index = 321

for nombre, (distribucion, parametros) in distribuciones.items():
    datos = generar_datos(distribucion, parametros, n_muestras)
    plt.subplot(subplot_index)
    
    for valor in datos:
        if nombre.startswith('tensiones'):
            a, b, c = valor, 0.1, 0.5
        else:
            a, b, c = 1, 0.1, valor
        plt.plot(x, curva_familia(x, a, b, c))
    
    plt.title(f'Curvas de Familia - {nombre.replace("_", " ").title()}')
    subplot_index += 1

plt.tight_layout()
plt.show()