import pygame
import os
from Bomba import Bomba

TILE_SIZE = 35
FOOTSTEP_SOUND = None
BOMB_SOUND = None

def carregar_so_bomba():
    global BOMB_SOUND
    if BOMB_SOUND is None:
        if not pygame.mixer.get_init():
            pygame.mixer.init()
        BOMB_SOUND = pygame.mixer.Sound(os.path.join("Assets", "Banda Sonora", "Bombs", "colocar_bomba.wav"))

def carregar_animacions_personatges():
    base_path = os.path.join("Assets", "players")
    animacions = {}
    mida_sprite = (150, 150)

    for nom_personatge in os.listdir(base_path):
        ruta_personatge = os.path.join(base_path, nom_personatge)
        if not os.path.isdir(ruta_personatge):
            continue

        animacions[nom_personatge] = {}

        for direccio in ["down", "up", "left", "right"]:
            ruta_direccio = os.path.join(ruta_personatge, direccio)
            if not os.path.isdir(ruta_direccio):
                continue

            frames = []
            for fitxer in sorted(os.listdir(ruta_direccio)):
                if fitxer.endswith(".png"):
                    ruta_imatge = os.path.join(ruta_direccio, fitxer)
                    imatge = pygame.image.load(ruta_imatge).convert_alpha()
                    imatge = pygame.transform.scale(imatge, mida_sprite)
                    frames.append(imatge)

            animacions[nom_personatge][direccio] = frames

    return animacions


def carregar_so_passos():
    global FOOTSTEP_SOUND
    if FOOTSTEP_SOUND is None:
        if not pygame.mixer.get_init():
            pygame.mixer.init()
        FOOTSTEP_SOUND = pygame.mixer.Sound(os.path.join("Assets", "Banda Sonora", "movimiento", "pasos.wav"))


class Personaje:
    POSICIONS_INICIALS = [(1, 1), (15, 19), (1, 19), (15, 1)]

    def __init__(self, fila, col, animacions, mapa, tipus, id_mando=None, direccio_inicial="down", velocitat=2):
        self.fila = fila
        self.col = col
        self.mapa = mapa
        self.velocitat = velocitat
        self.direccio = direccio_inicial

        self.tipus = tipus
        self.id_mando = id_mando

        self.animacions = animacions
        self.sprite_size = int(mapa.mida_casella * 1.5)
        self.mida = (self.sprite_size, self.sprite_size)
        self._escalar_frames()

        self.x = col * mapa.mida_casella + mapa.offset_left + (mapa.mida_casella - self.sprite_size) // 2
        self.y = fila * mapa.mida_casella + mapa.offset_top + (mapa.mida_casella - self.sprite_size) // 2

        self.dest_x = self.x
        self.dest_y = self.y

        self.bombes_actives = []

        self.frame_index = 0
        self.frame_timer = 0
        self.frame_delay = 150
        self.sprite_actual = self.animacions[self.direccio][0]
        self.sound_timer = 0
        self.sound_interval = 250  # mil·lisegons

        carregar_so_passos()
        self.footstep_sound = FOOTSTEP_SOUND

        carregar_so_bomba()
        self.bomb_sound = BOMB_SOUND

    @classmethod
    def crear_des_de_gestor(cls, mapa, noms_personatges):
        from GestorGlobal import gestor_jugadores
        animacions_personatges = carregar_animacions_personatges()
        jugadors = []
        posicions = cls.POSICIONS_INICIALS

        for idx, j in enumerate(gestor_jugadores.jugadores):
            indice = j.get("indice", 0)
            tipus = j.get("tipo", "teclado")
            id_mando = j.get("id") if tipus == "mando" else None

            if indice < len(noms_personatges):
                nom_personatge = noms_personatges[indice]
                if nom_personatge in animacions_personatges:
                    fila, col = posicions[idx]
                    anims = animacions_personatges[nom_personatge]
                    jugador = cls(fila, col, anims, mapa, tipus=tipus, id_mando=id_mando)
                    jugadors.append(jugador)

        return jugadors

    def _escalar_frames(self):
        for direccio in self.animacions:
            self.animacions[direccio] = [pygame.transform.scale(img, self.mida) for img in self.animacions[direccio]]

    def _actualitzar_sprite(self):
        self.frame_index = (self.frame_index + 1) % len(self.animacions[self.direccio])
        self.sprite_actual = self.animacions[self.direccio][self.frame_index]

    def move_up(self):
        if self.x == self.dest_x and self.y == self.dest_y:
            self.direccio = "up"
            self.dest_y -= self.mapa.mida_casella
            self.fila -= 1
            self._actualitzar_sprite()

    def move_down(self):
        if self.x == self.dest_x and self.y == self.dest_y:
            self.direccio = "down"
            self.dest_y += self.mapa.mida_casella
            self.fila += 1
            self._actualitzar_sprite()

    def move_left(self):
        if self.x == self.dest_x and self.y == self.dest_y:
            self.direccio = "left"
            self.dest_x -= self.mapa.mida_casella
            self.col -= 1
            self._actualitzar_sprite()

    def move_right(self):
        if self.x == self.dest_x and self.y == self.dest_y:
            self.direccio = "right"
            self.dest_x += self.mapa.mida_casella
            self.col += 1
            self._actualitzar_sprite()

    def moure(self, dx, dy):
        if dx != 0 and dy != 0:
            if abs(dx) > abs(dy):
                dy = 0
            else:
                dx = 0

        if dx == 0 and dy == 0:
            self.frame_index = 0
            return

        nova_fila = self.fila + dy
        nova_col = self.col + dx

        if self.mapa.es_bloquejada(nova_fila, nova_col):
            return

        if dx == 1:
            self.move_right()
        elif dx == -1:
            self.move_left()
        elif dy == -1:
            self.move_up()
        elif dy == 1:
            self.move_down()

    def update(self, dt):
        velocitat_px = self.velocitat

        moving = False

        if self.x < self.dest_x:
            self.x += velocitat_px
            if self.x > self.dest_x:
                self.x = self.dest_x
            moving = True
        elif self.x > self.dest_x:
            self.x -= velocitat_px
            if self.x < self.dest_x:
                self.x = self.dest_x
            moving = True

        if self.y < self.dest_y:
            self.y += velocitat_px
            if self.y > self.dest_y:
                self.y = self.dest_y
            moving = True
        elif self.y > self.dest_y:
            self.y -= velocitat_px
            if self.y < self.dest_y:
                self.y = self.dest_y
            moving = True

        if moving:
            self.frame_timer += dt
            self.sound_timer += dt
            if self.frame_timer >= self.frame_delay:
                self.frame_timer = 0
                frames = self.animacions[self.direccio]
                self.frame_index = (self.frame_index + 1) % (len(frames) - 1) + 1

            if self.sound_timer >= self.sound_interval:
                self.sound_timer = 0
                self.footstep_sound.play()
        else:
            self.frame_index = 0

        self.sprite_actual = self.animacions[self.direccio][self.frame_index]

        self.bombes_actives = [b for b in self.bombes_actives if not b.finalitzada]
        self.mapa.bombes_colocades = [b for b in self.mapa.bombes_colocades if not b.finalitzada]

    def colocar_bomba(self, llista_bombes):
        # Només permet col·locar si no ha arribat al límit
        MAX_BOMBES = 1  # pots augmentar aquest valor si tens power-ups
        self.bombes_actives = [b for b in self.bombes_actives if not b.finalitzada]
        if len(self.bombes_actives) >= MAX_BOMBES:
            return

        tile_x = (self.x - self.mapa.offset_left + TILE_SIZE // 2) // TILE_SIZE
        tile_y = (self.y - self.mapa.offset_top + TILE_SIZE // 2) // TILE_SIZE

        nova_bomba = Bomba(tile_x, tile_y, self.mapa)
        self.bombes_actives.append(nova_bomba)
        llista_bombes.append(nova_bomba)
        self.mapa.bombes_colocades.append(nova_bomba)

        if self.sound_timer >= self.sound_interval:
            self.sound_timer = 0
            self.bomb_sound.play()

    def dibuixar(self, screen):
        screen.blit(self.sprite_actual, (self.x, self.y))
