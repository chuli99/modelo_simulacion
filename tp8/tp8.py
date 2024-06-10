import pygame
import random
import numpy as np

#Inicialización de Pygame
pygame.init()

#Colores
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
ROJO = (255, 0, 0)
VERDE = (0, 255, 0)
AZUL = (0, 0, 255)

#Parámetros del sistema
CANT_CAJAS = int(input("Ingrese la cantidad de cajas:"))  
COSTO_CAJA = 1000
COSTO_PERDIDA_CLIENTE = 10000
HORAS_OPERACION = 4  
SEGUNDOS_POR_HORA = 3600
TIEMPO_TOTAL = HORAS_OPERACION * SEGUNDOS_POR_HORA
TIEMPO_ATENCION_MEDIA = 10 * 60  # 10 minutos en segundos
TIEMPO_ATENCION_DESV_EST = 5 * 60  # 5 minutos en segundos

#Parámetros de la distribución normal para la llegada de clientes
MEDIA_LLEGADA = 10 * 3600  # 10 horas en segundos
DESV_EST_LLEGADA = 2 * 3600  # 2 horas en segundos
LIMITE_INFERIOR = 8 * 3600  # 8 horas en segundos
LIMITE_SUPERIOR = 12 * 3600  # 12 horas en segundos

#Esperanza matemática de 100 personas en el transcurso de la mañana
CLIENTES_ESPERADOS = 100

#Configuración inicial de Pygame
ANCHO, ALTO = 800, 600
ventana = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption('Simulación de Servicio al Cliente')
reloj = pygame.time.Clock()

#Fuente y tamaño más pequeño
fuente_pequena = pygame.font.Font(None, 36)  # Tamaño más pequeño para los textos

#Variables de simulación
clientes = []
cajas = [None] * CANT_CAJAS
cola_espera = []
clientes_atendidos = 0
clientes_no_atendidos = 0
total_clientes = 0
tiempo_actual = 0
tiempos_atencion = []
tiempos_espera = []

#Función para generar tiempo de atención
def generar_tiempo_atencion():
    return max(1, int(random.gauss(TIEMPO_ATENCION_MEDIA, TIEMPO_ATENCION_DESV_EST)))

#Función para generar tiempos de llegada de clientes siguiendo una distribución normal truncada
def generar_tiempos_llegada(n, media, desviacion, limite_inferior, limite_superior):
    tiempos = []
    while len(tiempos) < n:
        tiempo = int(np.random.normal(media, desviacion))
        if limite_inferior <= tiempo <= limite_superior:
            tiempos.append(tiempo)
    return sorted(tiempos)

#Generar los tiempos de llegada de los clientes
tiempos_llegada_clientes = generar_tiempos_llegada(CLIENTES_ESPERADOS, MEDIA_LLEGADA, DESV_EST_LLEGADA, LIMITE_INFERIOR, LIMITE_SUPERIOR)

#Cliente
class Cliente:
    def __init__(self, tiempo_llegada):
        self.tiempo_llegada = tiempo_llegada
        self.tiempo_inicio_atencion = None
        self.tiempo_fin_atencion = None

    def iniciar_atencion(self, tiempo_inicio):
        self.tiempo_inicio_atencion = tiempo_inicio
        self.tiempo_fin_atencion = tiempo_inicio + generar_tiempo_atencion()
        tiempos_atencion.append(self.tiempo_fin_atencion - self.tiempo_inicio_atencion)

    def siendo_atendido(self, tiempo_actual):
        return self.tiempo_inicio_atencion is not None and self.tiempo_inicio_atencion <= tiempo_actual < self.tiempo_fin_atencion

    def atendido(self, tiempo_actual):
        return self.tiempo_fin_atencion is not None and self.tiempo_fin_atencion <= tiempo_actual

#Bucle principal de la simulación
while tiempo_actual < TIEMPO_TOTAL:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            tiempo_actual = TIEMPO_TOTAL
    
    #Llegada de nuevos clientes
    while tiempos_llegada_clientes and tiempos_llegada_clientes[0] <= tiempo_actual:
        tiempo_llegada = tiempos_llegada_clientes.pop(0)
        clientes.append(Cliente(tiempo_llegada))
        total_clientes += 1
    
    #Asignar clientes a cajas disponibles
    for cliente in clientes:
        if cliente.tiempo_inicio_atencion is None:
            for i in range(CANT_CAJAS):
                if cajas[i] is None:
                    cajas[i] = cliente
                    cliente.iniciar_atencion(tiempo_actual)
                    if cliente in cola_espera:
                        cola_espera.remove(cliente)
                    break
        elif cliente.atendido(tiempo_actual):
            for i in range(CANT_CAJAS):
                if cajas[i] == cliente:
                    cajas[i] = None
                    clientes.remove(cliente)
                    clientes_atendidos += 1
                    break
    
    #Gestionar cola de espera
    for cliente in clientes:
        if cliente.tiempo_inicio_atencion is None and cliente not in cola_espera:
            cola_espera.append(cliente)
        elif cliente.tiempo_inicio_atencion is None and (tiempo_actual - cliente.tiempo_llegada) >= 30 * 60:
            clientes_no_atendidos += 1
            clientes.remove(cliente)
    
    #Dibujar
    ventana.fill(BLANCO)
    
    #Dibujar texto "cajas"
    texto_cajas = fuente_pequena.render("Cajas", True, NEGRO)
    ventana.blit(texto_cajas, (50, 10))
    
    #Dibujar cajas
    for i in range(CANT_CAJAS):
        color = VERDE if cajas[i] is None else ROJO
        pygame.draw.rect(ventana, color, (50 + i * 70, 50, 60, 60))

    #Dibujar texto "clientes"
    texto_clientes = fuente_pequena.render("Clientes", True, NEGRO)
    ventana.blit(texto_clientes, (120, 140))
    
    #Dibujar clientes en la cola
    for i, cliente in enumerate(cola_espera):
        pygame.draw.circle(ventana, AZUL, (100, 150 + i * 30), 10)
    
    pygame.display.flip()
    reloj.tick(60)
    tiempo_actual += 1

pygame.quit()

#Calcular estadísticas
if tiempos_atencion:
    tiempo_min_atencion = min(tiempos_atencion)
    tiempo_max_atencion = max(tiempos_atencion)
else:
    tiempo_min_atencion = tiempo_max_atencion = 0

if tiempos_espera:
    tiempo_min_espera = min(tiempos_espera)
    tiempo_max_espera = max(tiempos_espera)
else:
    tiempo_min_espera = tiempo_max_espera = 0

#Resultados
print(f'Total de clientes: {total_clientes}')
print(f'Clientes atendidos: {clientes_atendidos}')
print(f'Clientes no atendidos: {clientes_no_atendidos}')
print(f'Tiempo mínimo de atención en caja: {tiempo_min_atencion / 60:.2f} minutos')
print(f'Tiempo máximo de atención en caja: {tiempo_max_atencion / 60:.2f} minutos')
print(f'Tiempo mínimo de espera en cola: {tiempo_min_espera / 60:.2f} minutos')
print(f'Tiempo máximo de espera en cola: {tiempo_max_espera / 60:.2f} minutos')
print(f'Costo de operación: {CANT_CAJAS * COSTO_CAJA + clientes_no_atendidos * COSTO_PERDIDA_CLIENTE}')