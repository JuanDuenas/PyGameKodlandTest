import pygame
import random
pygame.init
pygame.mixer.init()


size = (800, 500)

screen = pygame.display.set_mode([800, 500])
clock = pygame.time.Clock()
done = False

background = pygame.image.load("Resource/ImgBackground.jpg").convert()
pygame.mixer.music.load("Resource/SoundBackground.wav")
pygame.mixer.music.play(-1)

# Define la clase Nave
class Nave:
    def __init__(self, x, y, speed):
        # Inicializa la nave con su posición (x, y) y velocidad
        self.x = x
        self.y = y
        self.speed = speed
        # Carga la imagen de la navE
        imgNave = pygame.image.load("Resource/ImgNave.png")
        self.img = pygame.transform.scale(imgNave, (120, 120)).convert_alpha()

    def mover(self, keys):
        # Mueve la nave según las teclas presionadas
        if keys[pygame.K_a]:
            self.x -= self.speed  # Mueve a la izquierda
        if keys[pygame.K_d]:
            self.x += self.speed  # Mueve a la derecha
        if keys[pygame.K_w]:
            self.y -= self.speed  # Mueve hacia arriba
        if keys[pygame.K_s]:
            self.y += self.speed  # Mueve hacia abajo

    def dibujar(self, window):
        # Dibuja la nave en la ventana del juego
        window.blit(self.img, (self.x, self.y))

# Crea una instancia de la nave
nave = Nave(50, 50, 5)

# Bucle principal del juego
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True  # Termina el juego si se cierra la ventana

    # Obtiene las teclas presionadas
    keys = pygame.key.get_pressed()
    # Mueve la nave
    nave.mover(keys)

    # Dibuja el fondo y la nave
    screen.blit(background,[0,0])
    nave.dibujar(screen)

    # Actualiza la pantalla del juego
    pygame.display.flip()
    # Controla la velocidad del juego
    clock.tick(60)

# Cierra Pygame al final del juego
pygame.quit()