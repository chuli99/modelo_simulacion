import pygame
import random
import math

#Inicialización de Pygame
pygame.init()
ANCHO, ALTO = 800, 800
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption('Simulación de Partículas en un Conducto')
reloj = pygame.time.Clock()

#Colores
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
ROJO = (255, 0, 0)

#Parámetros del conducto
forma_conducto = 'circular'  
dimensiones_conducto = [400]  

if forma_conducto == 'circular':
    radio = dimensiones_conducto[0] // 2
elif forma_conducto == 'cuadrado':
    lado = dimensiones_conducto[0]
elif forma_conducto == 'rectangular':
    ancho, alto = dimensiones_conducto
else:
    print("Forma de conducto no reconocida")
    exit()

#Dimensiones de las partículas
TAM_MIN_PARTICULA = 5  #en píxeles
TAM_MAX_PARTICULA = 10  #en píxeles
TOLERANCIA_ADHERENCIA = 2  #Tolerancia de adherencia en píxeles
DISTANCIA_PARADA = 300  #Distancia al centro para detener la simulación

#Clase Partícula
class Particula:
    def __init__(self, pos_x, pos_y, tam):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.tam = tam

    def mover(self):
        direccion = random.choice(['arriba', 'abajo', 'izquierda', 'derecha'])
        if direccion == 'arriba':
            self.pos_y -= self.tam
        elif direccion == 'abajo':
            self.pos_y += self.tam
        elif direccion == 'izquierda':
            self.pos_x -= self.tam
        elif direccion == 'derecha':
            self.pos_x += self.tam

    def cerca_de_pared(self):
        if forma_conducto == 'circular':
            dist_al_centro = math.sqrt((self.pos_x - ANCHO // 2) ** 2 + (self.pos_y - ALTO // 2) ** 2)
            return dist_al_centro + self.tam // 2 >= radio
        elif forma_conducto == 'cuadrado':
            return (self.pos_x - self.tam // 2 <= 0 or self.pos_x + self.tam // 2 >= ANCHO or
                    self.pos_y - self.tam // 2 <= 0 or self.pos_y + self.tam // 2 >= ALTO)
        elif forma_conducto == 'rectangular':
            return (self.pos_x - self.tam // 2 <= 0 or self.pos_x + self.tam // 2 >= ANCHO or
                    self.pos_y - self.tam // 2 <= 0 or self.pos_y + self.tam // 2 >= ALTO)

    def cerca_de_particula(self, particulas):
        for particula in particulas:
            distancia = math.sqrt((self.pos_x - particula.pos_x) ** 2 + (self.pos_y - particula.pos_y) ** 2)
            if distancia <= self.tam + TOLERANCIA_ADHERENCIA:
                return True
        return False

#Lista de partículas adheridas
particulas = []

#Centro del conducto
centro_x = ANCHO // 2
centro_y = ALTO // 2

#Bucle principal
ejecutando = True
escala_tiempo = 1  # Escala de tiempo
while ejecutando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            ejecutando = False

    #Generar nueva partícula en el centro del conducto
    tam = random.randint(TAM_MIN_PARTICULA, TAM_MAX_PARTICULA)
    nueva_particula = Particula(centro_x, centro_y, tam)

    while True:
        nueva_particula.mover()

        if nueva_particula.cerca_de_pared() or nueva_particula.cerca_de_particula(particulas):
            particulas.append(nueva_particula)
            break

        #Detener la simulación si las partículas alcanzan una cierta distancia al centro
        dist_al_centro = math.sqrt((nueva_particula.pos_x - centro_x) ** 2 + (nueva_particula.pos_y - centro_y) ** 2)
        if dist_al_centro >= DISTANCIA_PARADA:
            ejecutando = False
            break

    #Dibujar
    pantalla.fill(BLANCO)

    #Dibujar conducto
    if forma_conducto == 'circular':
        pygame.draw.circle(pantalla, NEGRO, (centro_x, centro_y), radio, 2)
    elif forma_conducto == 'cuadrado':
        pygame.draw.rect(pantalla, NEGRO, (centro_x - lado // 2, centro_y - lado // 2, lado, lado), 2)
    elif forma_conducto == 'rectangular':
        pygame.draw.rect(pantalla, NEGRO, (centro_x - ancho // 2, centro_y - alto // 2, ancho, alto), 2)

    #Dibujar partículas adheridas
    for particula in particulas:
        pygame.draw.rect(pantalla, ROJO, (particula.pos_x - particula.tam // 2, particula.pos_y - particula.tam // 2, particula.tam, particula.tam))

    pygame.display.flip()
    reloj.tick(60 * escala_tiempo)

pygame.quit()
