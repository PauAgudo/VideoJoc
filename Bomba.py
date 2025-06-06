import pygame
import os
import math

TILE_SIZE = 35

class Bomba:
    def __init__(self, tile_x, tile_y, mapa, rang=2):
        self.tile_x = tile_x
        self.tile_y = tile_y
        self.mapa = mapa
        self.rang = rang
        self.temps_explosio = 3000  # ms
        self.inici = pygame.time.get_ticks()
        self.explotada = False

        self.frames_bomba = self._carregar_frames("bombas", "bomb", 15)
        self.frames_centre = self._carregar_frames("bombas", "bomba_c", 17)
        self.frames_extrem = self._carregar_frames("bombas", "ex_e", 17)
        self.frames_lateral = self._carregar_frames("bombas", "ex_l", 17)

        self.frame_index = 0
        self.frame_timer = 0
        self.frame_delay = 100  # ms entre frames de l'explosió
        self.finalitzada = False
        self.blocs_en_animacio = []

    def _carregar_frames(self, subcarpeta, prefix, total):
        ruta = os.path.join("Assets", subcarpeta)
        frames = []
        for i in range(1, total + 1):
            nom = f"{prefix}{i}.png"
            ruta_fitxer = os.path.join(ruta, nom)
            imatge = pygame.image.load(ruta_fitxer).convert_alpha()
            imatge = pygame.transform.scale(imatge, (TILE_SIZE, TILE_SIZE))
            frames.append(imatge)
        return frames

    def update(self):
        ara = pygame.time.get_ticks()
        if not self.explotada:
            if ara - self.inici >= self.temps_explosio:
                self.explotada = True
                self.frame_index = 0
                self.inici = ara
            else:
                if ara - self.inici >= self.frame_index * (self.temps_explosio // len(self.frames_bomba)):
                    self.frame_index = min(self.frame_index + 1, len(self.frames_bomba) - 1)
        else:
            if ara - self.inici >= self.frame_index * self.frame_delay:
                self.frame_index += 1

            # Avança animació de desaparició de blocs
            blocs_per_eliminar = []
            for i, (bx, by, index) in enumerate(self.blocs_en_animacio):
                if index >= len(self.frames_centre):
                    blocs_per_eliminar.append((bx, by))
            self.blocs_en_animacio = [(bx, by, idx + 1) for (bx, by, idx) in self.blocs_en_animacio]

            for bx, by in blocs_per_eliminar:
                self.mapa.grid[by][bx] = 0
                if (bx, by) in self.mapa.blocs_destruibles:
                    self.mapa.blocs_destruibles.remove((bx, by))

            if self.frame_index >= len(self.frames_centre):
                self.finalitzada = True

    def dibuixar(self, pantalla):
        if not self.explotada:
            imatge = self.frames_bomba[self.frame_index]
            escala = 1.0 + 0.1 * math.sin(pygame.time.get_ticks() / 100)
            nova_mida = int(TILE_SIZE * escala)
            imatge_escalada = pygame.transform.scale(imatge, (nova_mida, nova_mida))
            px = self.tile_x * TILE_SIZE + self.mapa.offset_left + (TILE_SIZE - nova_mida) // 2
            py = self.tile_y * TILE_SIZE + self.mapa.offset_top + (TILE_SIZE - nova_mida) // 2
            pantalla.blit(imatge_escalada, (px, py))
        elif not self.finalitzada:
            self._dibuixar_explosio(pantalla)

    def _dibuixar_explosio(self, pantalla):
        centre_img = self.frames_centre[self.frame_index % len(self.frames_centre)]
        px = self.tile_x * TILE_SIZE + self.mapa.offset_left
        py = self.tile_y * TILE_SIZE + self.mapa.offset_top
        pantalla.blit(centre_img, (px, py))

        direccions = {
            (0, -1): 0,
            (1, 0): -90,
            (0, 1): 180,
            (-1, 0): 90
        }


        if (self.tile_y, self.tile_x) in self.mapa.blocs_destruibles:
            if (self.tile_x, self.tile_y) not in [(b[0], b[1]) for b in self.blocs_en_animacio]:
                self.blocs_en_animacio.append((self.tile_x, self.tile_y, 0))

        for (dx, dy), angle in direccions.items():
            for i in range(1, self.rang + 1):
                tx = self.tile_x + dx * i
                ty = self.tile_y + dy * i

                if self.mapa.fora_limits(ty, tx):
                    break

                if (ty, tx) in self.mapa.blocs_destruibles:
                    if (tx, ty) not in [(b[0], b[1]) for b in self.blocs_en_animacio]:
                        self.blocs_en_animacio.append((tx, ty, 0))  # index inicial a 0
                    break

                if self.mapa.es_bloquejada(ty, tx):
                    break

                px = tx * TILE_SIZE + self.mapa.offset_left
                py = ty * TILE_SIZE + self.mapa.offset_top

                if i == self.rang:
                    frame = self.frames_extrem[self.frame_index % len(self.frames_extrem)]
                else:
                    frame = self.frames_lateral[self.frame_index % len(self.frames_lateral)]

                frame_rotat = pygame.transform.rotate(frame, angle)
                pantalla.blit(frame_rotat, (px, py))

        # Dibuixa l'animació de desaparició de blocs destructibles
        for (bx, by, index) in self.blocs_en_animacio:
            if index < len(self.frames_centre):
                img = self.frames_centre[index]
                px = bx * TILE_SIZE + self.mapa.offset_left
                py = by * TILE_SIZE + self.mapa.offset_top
                pantalla.blit(img, (px, py))