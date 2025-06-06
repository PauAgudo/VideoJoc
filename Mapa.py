import pygame
import os
import random


class Mapa:
    def __init__(self, mapa_id):
        # Dimensions del mapa en cel·les
        self.columnes = 21
        self.files = 17
        self.mida_casella = 35

        # Offsets per centrar el mapa i deixar espai pels marcadors
        self.offset_top = 80
        self.offset_left = 250
        self.offset_right = 250

        # Ruta base del mapa seleccionat
        base_path = os.path.join("Assets", "Mapas", f"Mapa{mapa_id}")

        # Carregar imatges dels tiles des de la carpeta del mapa
        self.terra1 = pygame.image.load(os.path.join(base_path, "tile1.png")).convert()
        self.terra2 = pygame.image.load(os.path.join(base_path, "tile2.png")).convert()
        self.mur = pygame.image.load(os.path.join(base_path, "muro.png")).convert()
        self.obstaculo = pygame.image.load(os.path.join(base_path, "obstacle.png")).convert()
        self.bloc_destruible = pygame.image.load(os.path.join(base_path, "destructible.png")).convert()

        # Bombas
        self.bombes_colocades = []

        # Escalat a mida de casella
        self.terra1 = pygame.transform.scale(self.terra1, (self.mida_casella, self.mida_casella))
        self.terra2 = pygame.transform.scale(self.terra2, (self.mida_casella, self.mida_casella))
        self.mur = pygame.transform.scale(self.mur, (self.mida_casella, self.mida_casella))
        self.obstaculo = pygame.transform.scale(self.obstaculo, (self.mida_casella, self.mida_casella))
        self.bloc_destruible = pygame.transform.scale(self.bloc_destruible, (self.mida_casella, self.mida_casella))

        # Matriu de col·lisions: 0 = lliure, 1 = mur fix, 2 = destructible
        self.grid = [[0 for _ in range(self.columnes)] for _ in range(self.files)]

        # Generar posicions dels blocs destructibles i marcar murs
        self.blocs_destruibles = set()
        self.generar_blocs_destruibles()

    def es_cantonada_segura(self, fila, col):
        return (
            (fila <= 2 and col <= 2) or
            (fila <= 2 and col >= self.columnes - 3) or
            (fila >= self.files - 3 and col <= 2) or
            (fila >= self.files - 3 and col >= self.columnes - 3)
        )

    def fora_limits(self, fila, col):
        files = len(self.grid)
        columnes = len(self.grid[0]) if files > 0 else 0
        return fila < 0 or fila >= files or col < 0 or col >= columnes

    def generar_blocs_destruibles(self):
        for fila in range(self.files):
            for col in range(self.columnes):
                # Murs de contorn
                if fila == 0 or fila == self.files - 1 or col == 0 or col == self.columnes - 1:
                    self.grid[fila][col] = 1
                # Obstacles interns en posicions parell-parell (excloent murs)
                elif fila % 2 == 0 and col % 2 == 0:
                    self.grid[fila][col] = 1
                # Possibles blocs destructibles
                elif not self.es_cantonada_segura(fila, col) and random.random() < 0.7:
                    self.blocs_destruibles.add((fila, col))
                    self.grid[fila][col] = 2

    def es_bloquejada(self, fila, col):
        if self.grid[fila][col] in (1, 2):
            return True
        for bomba in self.bombes_colocades:
            if not bomba.explotada and bomba.tile_x == col and bomba.tile_y == fila:
                return True
        return False

    def destrueix_bloc(self, fila, col):
        if (fila, col) in self.blocs_destruibles:
            self.blocs_destruibles.remove((fila, col))
            self.grid[fila][col] = 0

    def dibuixar(self, screen):
        for fila in range(self.files):
            for col in range(self.columnes):
                x = col * self.mida_casella + self.offset_left
                y = fila * self.mida_casella + self.offset_top

                # Alternar terra com escacat
                if (fila + col) % 2 == 0:
                    screen.blit(self.terra1, (x, y))
                else:
                    screen.blit(self.terra2, (x, y))

                # Dibuix segons tipus de cel·la
                if self.grid[fila][col] == 1:
                    if fila == 0 or fila == self.files - 1 or col == 0 or col == self.columnes - 1:
                        screen.blit(self.mur, (x, y))
                    else:
                        screen.blit(self.obstaculo, (x, y))
                elif self.grid[fila][col] == 2:
                    screen.blit(self.bloc_destruible, (x, y))
