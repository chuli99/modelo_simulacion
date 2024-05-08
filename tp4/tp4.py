import matplotlib.pyplot as plt
from calentador import Calentador
from const import *

calentador=Calentador(temperatura,masa,tiempo,voltaje)
resistencia = calentador.calculo_restistencia()
potencia = (voltaje ** 2) / resistencia
ticks_total = ticks_por_segundo

def temperatura_con_perdidas(ticks):
    temperatura = temperatura_inicial
    for _ in range(ticks):
        potencia_efectiva = resistencia - (temperatura - temperatura_inicial) * 10
        calor_suministrado = potencia_efectiva / ticks_por_segundo
        calor_absorbido = calor_fluido * masa_fluido
        delta_temperatura = calor_suministrado / calor_absorbido
        temperatura += delta_temperatura
    return temperatura

def temperatura_sin_perdidas(ticks):
    temperatura = temperatura_inicial
    for _ in range(ticks):
        calor_suministrado = resistencia / ticks_por_segundo
        calor_absorbido = calor_fluido * masa_fluido
        delta_temperatura = calor_suministrado / calor_absorbido
        temperatura += delta_temperatura
    return temperatura

temperaturas_con_perdidas = [temperatura_inicial]
temperaturas_sin_perdidas = [temperatura_inicial]

for tick in range(1, ticks_total + 1):
    temp_con_perdidas = temperatura_con_perdidas(tick)
    temp_sin_perdidas = temperatura_sin_perdidas(tick)
    temperaturas_con_perdidas.append(temp_con_perdidas)
    temperaturas_sin_perdidas.append(temp_sin_perdidas)

# lista de tiempo en segundos para cada tick
tiempo = [i / ticks_por_segundo for i in range(ticks_total + 1)]

# graficamos
plt.plot(tiempo, temperaturas_con_perdidas, label='Con perdida')
plt.plot(tiempo, temperaturas_sin_perdidas, label='Sin perdida')
plt.xlabel('Tiempo')
plt.ylabel('Temperatura del agua')
plt.title('Temperatura del agua en el calentador')
plt.legend()
plt.grid(True)
plt.show()