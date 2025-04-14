import pygame
import sys
import math

# --- Clase para el fondo animado ---
class BackgroundAnimation:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height

        # Cargar y escalar imágenes de fondo
        self.sky = pygame.image.load("imagenes/cielo.png").convert()
        self.sky = pygame.transform.scale(self.sky, (screen_width, screen_height))

        self.ground = pygame.image.load("imagenes/ground2.png").convert_alpha()
        self.ground_width, self.ground_height = self.ground.get_size()
        self.ground = pygame.transform.scale(self.ground, (screen_width, self.ground_height))

        self.cloud1 = pygame.image.load("imagenes/nube2.png").convert_alpha()
        self.cloud2 = pygame.image.load("imagenes/nube3.png").convert_alpha()
        self.cloud1 = pygame.transform.scale(self.cloud1, (120, 60))
        self.cloud2 = pygame.transform.scale(self.cloud2, (200, 100))
        self.cloud1_width = self.cloud1.get_width()
        self.cloud2_width = self.cloud2.get_width()

        # Posiciones iniciales
        self.cloud1_x = screen_width
        self.cloud1_y = 50
        self.cloud2_x = -self.cloud2_width
        self.cloud2_y = 80

        self.zeppelin = pygame.image.load("imagenes/zeppelin.png").convert_alpha()
        self.zeppelin = pygame.transform.scale(self.zeppelin, (300, 150))
        self.zeppelin_width = self.zeppelin.get_width()
        self.zeppelin_x = screen_width
        self.zeppelin_y = 130

        # Velocidades
        self.ground_speed = 2
        self.cloud1_speed = 1
        self.cloud2_speed = 0.5
        self.zeppelin_speed = 0.85
        self.ground_x = 0


    def update(self):
        # Actualizar posiciones
        self.cloud1_x += self.cloud1_speed
        if self.cloud1_x > self.screen_width:
            self.cloud1_x = -self.cloud1_width

        self.cloud2_x += self.cloud2_speed
        if self.cloud2_x > self.screen_width:
            self.cloud2_x = -self.cloud2_width

        self.zeppelin_x -= self.zeppelin_speed
        if self.zeppelin_x < -self.zeppelin_width:
            self.zeppelin_x = self.screen_width

        self.ground_x = (self.ground_x + self.ground_speed) % self.screen_width

    def draw(self, screen):
        # Dibujar en el orden deseado
        screen.blit(self.sky, (0, 0))
        screen.blit(self.cloud1, (self.cloud1_x, self.cloud1_y))
        screen.blit(self.cloud2, (self.cloud2_x, self.cloud2_y))
        screen.blit(self.zeppelin, (self.zeppelin_x, self.zeppelin_y))
        screen.blit(self.ground, (self.ground_x - self.screen_width, self.screen_height - self.ground_height))
        screen.blit(self.ground, (self.ground_x, self.screen_height - self.ground_height))


# --- Función para dibujar el texto con efecto de bombeo ---
def draw_bombeo_texto(screen, center, font, message):
    # Usamos el tiempo actual para calcular el factor de escala
    tiempo = pygame.time.get_ticks() / 300.0  # Ajusta la velocidad del efecto
    factor = 1 + 0.05 * math.sin(tiempo)  # Oscila entre 0.95 y 1.05 aproximadamente
    texto_render = font.render(message, True, (255, 255, 255))
    new_width = int(texto_render.get_width() * factor)
    new_height = int(texto_render.get_height() * factor)
    texto_escala = pygame.transform.scale(texto_render, (new_width, new_height))
    rect = texto_escala.get_rect(center=center)
    screen.blit(texto_escala, rect)


# --- Pantalla de inicio (background con texto animado) ---
def background_screen(screen):
    pygame.init()
    screen_width, screen_height = 800, 600
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Pantalla de Inicio - Fondo Animado")
    clock = pygame.time.Clock()

    # Configurar la fuente y parámetros del texto
    font = pygame.font.SysFont("Arial", 26)
    message = "Pulsa cualquier tecla para continuar"
    text_center = (screen_width // 2, screen_height - 100)

    # Cargar efecto sonido
    key_sound = pygame.mixer.Sound("media/interface.mp3")
    key_sound.set_volume(1)  # volumen al 100%

    # Crear la instancia del fondo animado
    bg_anim = BackgroundAnimation(screen_width, screen_height)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit();
                sys.exit()
            # Al pulsar cualquier tecla se cambia a la siguiente pantalla
            if event.type == pygame.KEYDOWN:
                key_sound.play()
                running = False

        bg_anim.update()
        bg_anim.draw(screen)
        draw_bombeo_texto(screen, text_center, font, message)
        pygame.display.flip()
        clock.tick(60)

    return bg_anim  # Retornamos el estado del fondo para usarlo como base


