import numpy as np
import matplotlib.pyplot as plt

def resistencia_uniforme():
    return np.random.uniform(1, 10, 5)

def temperatura_normal():
    return np.random.normal(10, 5, 5)

def temperatura_ambiente_uniforme():
    return np.random.uniform(-20, 50, 8)

def tension_alimentacion_normal(option=1):
    if option == 1:
        return np.random.normal(12, 4, 5)
    elif option == 2:
        return np.random.normal(220, 40, 5)

def curva_familia(x, parametros):
    a, b, c = parametros
    return a * np.exp(b * x) + c  

# Generar datos para las curvas de familia
resistencias = resistencia_uniforme()
temperaturas_agua = temperatura_normal()
temperaturas_ambiente = temperatura_ambiente_uniforme()
tensiones_alimentacion_1 = tension_alimentacion_normal(option=1)
tensiones_alimentacion_2 = tension_alimentacion_normal(option=2)

x = np.linspace(0, 10, 100)

# Graficar las curvas de familia
plt.figure(figsize=(10, 8))

# Curvas de resistencia
plt.subplot(321)
for resistencia in resistencias:
    parametros = [resistencia, 0.1, 0.5]
    plt.plot(x, curva_familia(x, parametros))
plt.title('Curvas de Familia - Resistencias')

# Curvas de temperatura del agua
plt.subplot(322)
for temperatura in temperaturas_agua:
    parametros = [1, 0.1, temperatura]
    plt.plot(x, curva_familia(x, parametros))
plt.title('Curvas de Familia - Temperatura del Agua')

# Curvas de temperatura del ambiente
plt.subplot(323)
for temperatura in temperaturas_ambiente:
    parametros = [1, 0.1, temperatura]
    plt.plot(x, curva_familia(x, parametros))
plt.title('Curvas de Familia - Temperatura del Ambiente')

# Curvas de tensión de alimentación
plt.subplot(324)
for tension in tensiones_alimentacion_1:
    parametros = [tension, 0.1, 0.5]
    plt.plot(x, curva_familia(x, parametros))
plt.title('Curvas de Familia - Tensión de Alimentación (Media 12)')

# Curvas de tensión de alimentación
plt.subplot(325)
for tension in tensiones_alimentacion_2:
    parametros = [tension, 0.1, 0.5]
    plt.plot(x, curva_familia(x, parametros))
plt.title('Curvas de Familia - Tensión de Alimentación (Media 220)')

plt.tight_layout()
plt.show()