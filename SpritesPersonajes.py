import pygame
import os
from ConfiguraciónMandos import gestor_jugadores

TILE_SIZE = 35


def carregar_animacions_personatges():
    base_path = os.path.join("Assets", "players")
    animacions = {}

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
                    frames.append(imatge)

            animacions[nom_personatge][direccio] = frames

    return animacions


class Personaje:
    POSICIONS_INICIALS = [(1, 1), (15, 19), (1, 19), (15, 1)]

    def __init__(self, fila, col, animacions, mapa, tipus, id_mando=None, direccio_inicial="down", velocitat=2):
        self.fila = fila
        self.col = col
        self.mapa = mapa
        self.velocitat = velocitat
        self.direccio = direccio_inicial

        self.tipus = tipus  # "teclat" o "mando"
        self.id_mando = id_mando  # només si tipus == "mando"

        self.animacions = animacions
        self.sprite_size = int(mapa.mida_casella * 1.5)
        self.mida = (self.sprite_size, self.sprite_size)
        self._escalar_frames()

        self.x = col * mapa.mida_casella + mapa.offset_left + (mapa.mida_casella - self.sprite_size) // 2
        self.y = fila * mapa.mida_casella + mapa.offset_top + (mapa.mida_casella - self.sprite_size) // 2

        self.dest_x = self.x
        self.dest_y = self.y

        self.frame_index = 0
        self.frame_timer = 0
        self.frame_delay = 150
        self.sprite_actual = self.animacions[self.direccio][0]

    @classmethod
    def crear_des_de_gestor(cls, mapa, noms_personatges):
        animacions_personatges = carregar_animacions_personatges()
        jugadors = []

        for idx, j in enumerate(gestor_jugadores.jugadores):
            indice = j.get("indice", 0)
            tipus = j.get("tipus", "teclat")
            id_mando = j.get("id") if tipus == "mando" else None

            if indice < len(noms_personatges):
                nom_personatge = noms_personatges[indice]
                if nom_personatge in animacions_personatges:
                    fila, col = cls.POSICIONS_INICIALS[idx]
                    anims = animacions_personatges[nom_personatge]
                    jugador = cls(fila, col, anims, mapa, tipus, id_mando)
                    jugadors.append(jugador)

        return jugadors

    def _escalar_frames(self):
        for direccio in self.animacions:
            self.animacions[direccio] = [pygame.transform.scale(img, self.mida) for img in self.animacions[direccio]]

    def moure(self, dx, dy):
        if dx == 0 and dy == 0:
            return

        if dx == 1:
            self.direccio = "right"
        elif dx == -1:
            self.direccio = "left"
        elif dy == -1:
            self.direccio = "up"
        elif dy == 1:
            self.direccio = "down"

        nova_fila = self.fila + dy
        nova_col = self.col + dx

        if 0 <= nova_fila < self.mapa.files and 0 <= nova_col < self.mapa.columnes:
            if not self.mapa.es_bloquejada(nova_fila, nova_col):
                self.fila = nova_fila
                self.col = nova_col
                self.dest_x = self.col * self.mapa.mida_casella + self.mapa.offset_left + (self.mapa.mida_casella - self.sprite_size) // 2
                self.dest_y = self.fila * self.mapa.mida_casella + self.mapa.offset_top + (self.mapa.mida_casella - self.sprite_size) // 2

    def update(self, dt):
        velocitat_px = self.velocitat

        if self.x < self.dest_x:
            self.x += velocitat_px
            if self.x > self.dest_x:
                self.x = self.dest_x
        elif self.x > self.dest_x:
            self.x -= velocitat_px
            if self.x < self.dest_x:
                self.x = self.dest_x

        if self.y < self.dest_y:
            self.y += velocitat_px
            if self.y > self.dest_y:
                self.y = self.dest_y
        elif self.y > self.dest_y:
            self.y -= velocitat_px
            if self.y < self.dest_y:
                self.y = self.dest_y

        if self.x != self.dest_x or self.y != self.dest_y:
            self.frame_timer += dt
            if self.frame_timer >= self.frame_delay:
                self.frame_timer = 0
                self.frame_index = (self.frame_index + 1) % len(self.animacions[self.direccio])
        else:
            self.frame_index = 0

        self.sprite_actual = self.animacions[self.direccio][self.frame_index]

    def dibuixar(self, screen):
        screen.blit(self.sprite_actual, (self.x, self.y))
