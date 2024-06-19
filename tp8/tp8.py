import pygame
import random

# Configuración inicial de Pygame
pygame.init()
ANCHO, ALTO = 800, 600
ventana = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption('Simulación de Sistema de Servicio al Cliente')
reloj = pygame.time.Clock()

# Colores
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
ROJO = (255, 0, 0)
VERDE = (0, 255, 0)
AZUL = (0, 0, 255)

# Parámetros del sistema
CANTIDAD_CAJAS = int(input("Ingrese el número de cajas:"))  # Puede ser de 1 a 10
COSTO_CAJA = 1000
COSTO_CLIENTE_PERDIDO = 10000
HORAS_OPERACION = 4  # De 8 a 12 horas
SEGUNDOS_POR_HORA = 3600
SEGUNDOS_TOTALES = HORAS_OPERACION * SEGUNDOS_POR_HORA
PROB_LLEGADA = 1 / 144
TIEMPO_MIN_ATENCION = 5 * 60  # 5 minutos en segundos
TIEMPO_MAX_ATENCION = 15 * 60  # 15 minutos en segundos
TIEMPO_CIERRE = 12 * SEGUNDOS_POR_HORA

# Variables de simulación
clientes = []
cajas = [None] * CANTIDAD_CAJAS
cola_espera = []
clientes_atendidos = 0
clientes_no_atendidos = 0
clientes_totales = 0
tiempo_actual = 0
tiempos_atencion = []
tiempos_espera = []

# Función para generar tiempo de atención
def generar_tiempo_atencion():
    return int(random.uniform(TIEMPO_MIN_ATENCION, TIEMPO_MAX_ATENCION))

# Cliente
class Cliente:
    def __init__(self, tiempo_llegada):
        self.tiempo_llegada = tiempo_llegada
        self.tiempo_inicio_atencion = None
        self.tiempo_fin_atencion = None

    def iniciar_atencion(self, tiempo_inicio):
        self.tiempo_inicio_atencion = tiempo_inicio
        self.tiempo_fin_atencion = tiempo_inicio + generar_tiempo_atencion()
        tiempos_atencion.append(self.tiempo_fin_atencion - self.tiempo_inicio_atencion)

    def esta_siendosiendo_atendido(self, tiempo_actual):
        return self.tiempo_inicio_atencion is not None and self.tiempo_inicio_atencion <= tiempo_actual < self.tiempo_fin_atencion

    def esta_atendido(self, tiempo_actual):
        return self.tiempo_fin_atencion is not None and tiempo_actual >= self.tiempo_fin_atencion

# Bucle principal
ejecutando = True
frames = []  # Lista para almacenar los fotogramas de la simulación
while ejecutando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            ejecutando = False

    # Generar nuevos clientes
    if random.random() < PROB_LLEGADA and tiempo_actual <= SEGUNDOS_TOTALES:
        clientes.append(Cliente(tiempo_actual))
        clientes_totales += 1

    # Asignar clientes a cajas libres
    for i in range(CANTIDAD_CAJAS):
        if cajas[i] is None and cola_espera:
            cliente = cola_espera.pop(0)
            cliente.iniciar_atencion(tiempo_actual)
            cajas[i] = cliente
            tiempos_espera.append(tiempo_actual - cliente.tiempo_llegada)

    # Procesar clientes en cajas
    for i in range(CANTIDAD_CAJAS):
        if cajas[i] is not None:
            if cajas[i].esta_atendido(tiempo_actual):
                cajas[i] = None
                clientes_atendidos += 1

    # Mover clientes a la cola
    for cliente in clientes[:]:
        if not cliente.esta_siendosiendo_atendido(tiempo_actual):
            if tiempo_actual - cliente.tiempo_llegada >= 30 * 60:
                clientes_no_atendidos += 1
                clientes.remove(cliente)
            elif cliente not in cola_espera and cliente.tiempo_inicio_atencion is None:
                cola_espera.append(cliente)

    # Dibujar
    ventana.fill(BLANCO)
    # Dibujar cajas
    for i in range(CANTIDAD_CAJAS):
        color = VERDE if cajas[i] is None else ROJO
        pygame.draw.rect(ventana, color, (50 + i * 70, 50, 60, 60))

    # Dibujar clientes en la cola
    for i, cliente in enumerate(cola_espera):
        pygame.draw.circle(ventana, AZUL, (100, 150 + i * 30), 10)

    pygame.display.flip()
    reloj.tick(60)

    # Avanzar el tiempo solo si la simulación está dentro del tiempo de apertura
    if tiempo_actual <= SEGUNDOS_TOTALES:
        tiempo_actual += 1
        # Agregar el fotograma actual a la lista de fotogramas
        frames.append(pygame.surfarray.array3d(ventana))
    else:
        ejecutando = False

pygame.quit()

# Calcular estadísticas
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

# Resultados
print(f'Total de clientes: {clientes_totales}')
print(f'Clientes atendidos: {clientes_atendidos}')
print(f'Clientes no atendidos: {clientes_no_atendidos}')
print(f'Clientes en el box: {clientes_totales-clientes_no_atendidos-clientes_atendidos}')
print(f'Tiempo mínimo de atención en box: {tiempo_min_atencion / 60:.2f} segundos')
print(f'Tiempo máximo de atención en box: {tiempo_max_atencion / 60:.2f} segundos')
print(f'Tiempo mínimo de espera en salón: {tiempo_min_espera / 60:.2f} segundos')
print(f'Tiempo máximo de espera en salón: {tiempo_max_espera / 60:.2f} segundos')
print(f'Costo de operación: {CANTIDAD_CAJAS * COSTO_CAJA + clientes_no_atendidos * COSTO_CLIENTE_PERDIDO}')
