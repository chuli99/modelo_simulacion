import matplotlib.pyplot as plt

fig, ax = plt.subplots()



p = 1114.6
temperatura_inicial = 20
temperatura = temperatura_inicial
c = 4186
i = 0
q = p*1
dT = q/(1*4186) 
lista_tiempo = []
lista_temperatura = []
while i < 300:
    temperatura = temperatura + dT
    lista_temperatura.append(temperatura)
    print(temperatura)
    lista_tiempo.append(i)
    i = i+1

ax.plot(lista_tiempo,lista_temperatura)
plt.show()