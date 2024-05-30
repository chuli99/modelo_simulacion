import pygame
import random

# Inicialización de Pygame
pygame.init()

# Colores
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
ROJO = (255, 0, 0)
VERDE = (0, 255, 0)
AZUL = (0, 0, 255)

# Parámetros del sistema
CANT_CAJAS = int(input("Ingrese la cantidad de cajas:"))  # Puede ser de 1 a 10
COSTO_CAJA = 1000
COSTO_PERDIDA_CLIENTE = 10000
HORAS_OPERACION = 4  # De 8 a 12 horas
SEGUNDOS_POR_HORA = 3600
TIEMPO_TOTAL = HORAS_OPERACION * SEGUNDOS_POR_HORA
PROBABILIDAD_LLEGADA = 1 / 144
TIEMPO_ATENCION_MEDIA = 10 * 60  # 10 minutos en segundos
TIEMPO_ATENCION_DESV_EST = 5 * 60  # 5 minutos en segundos

# Configuración inicial de Pygame
ANCHO, ALTO = 800, 600
ventana = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption('Simulación de Servicio al Cliente')
reloj = pygame.time.Clock()

# Fuente y tamaño más pequeño
fuente_pequena = pygame.font.Font(None, 36)  # Tamaño más pequeño para los textos

# Variables de simulación
clientes = []
cajas = [None] * CANT_CAJAS
cola_espera = []
clientes_atendidos = 0
clientes_no_atendidos = 0
total_clientes = 0
tiempo_actual = 0
tiempos_atencion = []
tiempos_espera = []

# Función para generar tiempo de atención
def generar_tiempo_atencion():
    return max(1, int(random.gauss(TIEMPO_ATENCION_MEDIA, TIEMPO_ATENCION_DESV_EST)))

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

    def siendo_atendido(self, tiempo_actual):
        return self.tiempo_inicio_atencion is not None and self.tiempo_inicio_atencion <= tiempo_actual < self.tiempo_fin_atencion

    def atendido(self, tiempo_actual):
        return self.tiempo_fin_atencion is not None and tiempo_actual >= self.tiempo_fin_atencion

# Bucle principal
ejecutando = True
while ejecutando and tiempo_actual <= TIEMPO_TOTAL:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            ejecutando = False

    # Generar nuevos clientes
    if random.random() < PROBABILIDAD_LLEGADA:
        clientes.append(Cliente(tiempo_actual))
        total_clientes += 1

    # Asignar clientes a cajas libres
    for i in range(CANT_CAJAS):
        if cajas[i] is None and cola_espera:
            cliente = cola_espera.pop(0)
            cliente.iniciar_atencion(tiempo_actual)
            cajas[i] = cliente
            tiempos_espera.append(tiempo_actual - cliente.tiempo_llegada)

    # Procesar clientes en cajas
    for i in range(CANT_CAJAS):
        if cajas[i] is not None:
            if cajas[i].atendido(tiempo_actual):
                cajas[i] = None
                clientes_atendidos += 1

    # Mover clientes a la cola
    for cliente in list(clientes):  # Iterar sobre una copia de la lista de clientes
        if not cliente.siendo_atendido(tiempo_actual):
            if tiempo_actual - cliente.tiempo_llegada >= 30 * 60:
                clientes_no_atendidos += 1
                clientes.remove(cliente)
            elif cliente not in cola_espera and cliente.tiempo_inicio_atencion is None:
                cola_espera.append(cliente)

    # Dibujar
    ventana.fill(BLANCO)
    
    # Dibujar texto "cajas"
    texto_cajas = fuente_pequena.render("Cajas", True, NEGRO)
    ventana.blit(texto_cajas, (50, 10))
    
    # Dibujar cajas
    for i in range(CANT_CAJAS):
        color = VERDE if cajas[i] is None else ROJO
        pygame.draw.rect(ventana, color, (50 + i * 70, 50, 60, 60))

    # Dibujar texto "clientes"
    texto_clientes = fuente_pequena.render("Clientes", True, NEGRO)
    ventana.blit(texto_clientes, (120, 140))
    
    # Dibujar clientes en la cola
    for i, cliente in enumerate(cola_espera):
        pygame.draw.circle(ventana, AZUL, (100, 150 + i * 30), 10)

    pygame.display.flip()
    reloj.tick(60)
    tiempo_actual += 1

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
print(f'Total de clientes: {total_clientes}')
print(f'Clientes atendidos: {clientes_atendidos}')
print(f'Clientes no atendidos: {clientes_no_atendidos}')
print(f'Tiempo mínimo de atención en caja: {tiempo_min_atencion / 60:.2f} minutos')
print(f'Tiempo máximo de atención en caja: {tiempo_max_atencion / 60:.2f} minutos')
print(f'Tiempo mínimo de espera en cola: {tiempo_min_espera / 60:.2f} minutos')
print(f'Tiempo máximo de espera en cola: {tiempo_max_espera / 60:.2f} minutos')
print(f'Costo de operación: {CANT_CAJAS * COSTO_CAJA + clientes_no_atendidos * COSTO_PERDIDA_CLIENTE}')
