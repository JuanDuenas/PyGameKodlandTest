import pygame
import random
import math

pygame.init()
pygame.mixer.init()

size = (800, 500)

screen = pygame.display.set_mode([800, 500])

clock = pygame.time.Clock()
done = False

background = pygame.image.load("Resource/ImgBackground.jpg").convert()
background_copy = background.copy()
pygame.mixer.music.load("Resource/SoundBackground.wav")
pygame.mixer.music.play(-1)
shoot_sound = pygame.mixer.Sound("Resource/SoundShoot.mp3")
impact_sound = pygame.mixer.Sound("Resource/SoundImpact.mp3")
game_over_image = pygame.image.load("Resource/ImgGameOver.png").convert_alpha()

def tutorial():
    screen.blit(background_copy, [0, 0])
    overlay = pygame.Surface((800, 500), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 128))
    screen.blit(overlay, (0, 0))
    tutorial_text = [
        "Para moverte presiona:",
        "Arriba 'W'",
        "Abajo 'S'",
        "Izquierda 'A'",
        "Derecha 'D'",
        "Para disparar, apunta con el mouse y dispara."
    ]
    font = pygame.font.Font(None, 24)
    text_y = 100
    for line in tutorial_text:
        text = font.render(line, True, (255, 255, 255))
        text_rect = text.get_rect(center=(400, text_y))
        screen.blit(text, text_rect)
        text_y += text.get_height() + 5

    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                return


def menu():
    while True:
        screen.blit(background_copy, [0, 0])
        overlay = pygame.Surface((800, 500), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 128))
        screen.blit(overlay, (0, 0))

        font = pygame.font.Font(None, 36)
        text_jugar = font.render("JUGAR", True, (255, 255, 255))
        text_tutorial = font.render("TUTORIAL", True, (255, 255, 255))
        text_salir = font.render("SALIR", True, (255, 255, 255))
        text_rect_jugar = text_jugar.get_rect(center=(400, 225))
        text_rect_tutorial = text_tutorial.get_rect(center=(400, 300))
        text_rect_salir = text_salir.get_rect(center=(400, 375))
        screen.blit(text_jugar, text_rect_jugar)
        screen.blit(text_tutorial, text_rect_tutorial)
        screen.blit(text_salir, text_rect_salir)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                if 300 <= mx <= 500 and 200 <= my <= 250:  # JUGAR
                    return "JUGAR"
                elif 300 <= mx <= 500 and 275 <= my <= 325:  # TUTORIAL
                    tutorial()
                elif 300 <= mx <= 500 and 350 <= my <= 400:  # SALIR
                    pygame.quit()
                    quit()


option = menu()


invulnerable_time = 3000
start_time = pygame.time.get_ticks()
nave_invulnerable = True

class Nave:
    def __init__(self, x, y, speed):
        self.x = x
        self.y = y
        self.speed = speed
        self.img_original = pygame.image.load("Resource/ImgNave.png").convert_alpha()
        self.img = self.img_original
        self.angle = 0

    def mover(self, keys):
        if keys[pygame.K_a]:
            self.x -= self.speed
        if keys[pygame.K_d]:
            self.x += self.speed
        if keys[pygame.K_w]:
            self.y -= self.speed
        if keys[pygame.K_s]:
            self.y += self.speed

    def rotar(self):
        mx, my = pygame.mouse.get_pos()
        self.angle = -math.degrees(math.atan2(self.y - my, self.x - mx)) + 90
        self.img = pygame.transform.rotate(self.img_original, self.angle)

    def dibujar(self, window):
        window.blit(self.img, (self.x - self.img.get_width() // 2, self.y - self.img.get_height() // 2))


nave = Nave(50, 50, 5)


class Asteroide:
    def __init__(self, x, y, speed_x, speed_y):
        self.x = x
        self.y = y
        self.speed_x = speed_x
        self.speed_y = speed_y
        imgAsteroide = pygame.image.load("Resource/ImgAst1.png")
        self.img = pygame.transform.scale(imgAsteroide, (50, 50)).convert_alpha()

    def mover(self):
        self.x += self.speed_x
        self.y += self.speed_y

    def dibujar(self, window):
        window.blit(self.img, (self.x, self.y))


asteroides = [Asteroide(random.randrange(800), random.randrange(500), random.choice([-2, 2]), random.choice([-2, 2]))
              for _ in range(10)]

class Disparo:
    def __init__(self, x, y, angle, speed):
        self.x = x
        self.y = y
        self.angle = angle
        self.speed = speed
        self.img = pygame.image.load("Resource/ImgLightBall.png").convert_alpha()

    def mover(self):
        self.x += math.cos(math.radians(self.angle + 90)) * self.speed
        self.y -= math.sin(math.radians(self.angle + 90)) * self.speed

    def dibujar(self, window):
        window.blit(self.img, (self.x - self.img.get_width() // 2, self.y - self.img.get_height() // 2))


disparos = []


while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            disparos.append(Disparo(nave.x, nave.y, nave.angle, 10))
            shoot_sound.play()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                option = menu()

    keys = pygame.key.get_pressed()
    nave.mover(keys)
    nave.rotar()

    current_time = pygame.time.get_ticks()
    if nave_invulnerable and current_time - start_time >= invulnerable_time:
        nave_invulnerable = False  # La nave ya no es invulnerable después de 3 segundos


    for asteroide in asteroides:
        asteroide.mover()
    for disparo in disparos:
        disparo.mover()

    if not nave_invulnerable:
        for asteroide in asteroides:
            if pygame.Rect(nave.x, nave.y, nave.img.get_width(), nave.img.get_height()).colliderect(
                    pygame.Rect(asteroide.x, asteroide.y, asteroide.img.get_width(), asteroide.img.get_height())):
                if current_time - start_time >= invulnerable_time:
                    screen.blit(game_over_image, (size[0] // 2 - game_over_image.get_width() // 2,
                                                  size[1] // 2 - game_over_image.get_height() // 2))
                    pygame.display.flip()
                    pygame.time.delay(2000)
                    option = menu()
                    nave.x = 50
                    nave.y = 50
                    asteroides = [Asteroide(random.randrange(800), random.randrange(500), random.choice([-2, 2]),
                                            random.choice([-2, 2])) for _ in range(10)]
                break


    if random.randrange(100) < 2:
        if random.choice([True, False]):
            x = random.choice([0, 800])
            y = random.randrange(500)
            speed_x = 2 if x == 0 else -2
            speed_y = random.choice([-2, 2])
        else:
            x = random.randrange(800)
            y = random.choice([0, 500])
            speed_x = random.choice([-2, 2])
            speed_y = 2 if y == 0 else -2  #
        asteroides.append(Asteroide(x, y, speed_x, speed_y))

    screen.blit(background, [0, 0])
    nave.dibujar(screen)

    for asteroide in asteroides:
        asteroide.dibujar(screen)
    for disparo in disparos:
        disparo.dibujar(screen)


    for disparo in disparos.copy():
        for asteroide in asteroides.copy():
            if math.hypot(disparo.x - asteroide.x, disparo.y - asteroide.y) < 50:
                asteroides.remove(asteroide)
                disparos.remove(disparo)
                impact_sound.play()
                break

    pygame.display.flip()
    clock.tick(60)
