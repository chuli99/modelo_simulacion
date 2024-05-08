#Datos necesarios
indice_conductividad = 0.035
sup = 0.035
espesor = 0.01

#Obtengo valor de perdida
perdida = indice_conductividad*sup/espesor

#Muestro perdida
print(f"El valor de perdida es de: {perdida}")