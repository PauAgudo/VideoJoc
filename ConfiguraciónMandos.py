# CLASE PARA GESTIONAR JUGADORES Y MANDOS

import pygame

class GestorJugadores:
    def __init__(self):
        self.jugadores = []  # Lista de dicts: tipo ("teclado"/"mando"), id, indice personaje
        self.max_jugadores = 4

    def reset(self):
        self.jugadores.clear()

    def unir_teclado(self):
        if not any(j["tipo"] == "teclado" for j in self.jugadores) and len(self.jugadores) < self.max_jugadores:
            nuevo_id = f"J{len(self.jugadores) + 1}"  # Asignar identificador dinámico

            self.jugadores.append({
                "tipo": "teclado",
                "id": None,
                "instance_id": "teclado",
                "indice": 0,
                "id_jugador": nuevo_id
            })
            return len(self.jugadores)
        return None

    def unir_mando(self, device_index):
        joy = pygame.joystick.Joystick(device_index)
        if not joy.get_init():
            joy.init()

        instance_id = joy.get_instance_id()
        if not any(j.get("instance_id") == instance_id for j in self.jugadores) and len(
                self.jugadores) < self.max_jugadores:
            nuevo_id = f"J{len(self.jugadores) + 1}"

            self.jugadores.append({
                "tipo": "mando",
                "id": device_index,  # lo conservamos por si hace falta
                "instance_id": instance_id,  # ¡el que nunca cambia!
                "indice": 0,
                "id_jugador": nuevo_id
            })
            return len(self.jugadores)
        return None

    def actualizar_indice(self, jugador_index, nuevo_indice):
        if 0 <= jugador_index < len(self.jugadores):
            self.jugadores[jugador_index]["indice"] = nuevo_indice

    def get_jugador_por_joy(self, instance_id):
        for j in self.jugadores:
            if j.get("instance_id") == instance_id:
                return j
        return None

    def get_teclado(self):
        for j in self.jugadores:
            if j["tipo"] == "teclado":
                return j
        return None

    def get(self, index):
        if index < len(self.jugadores):
            return self.jugadores[index]
        return None

    def todos(self):
        return self.jugadores

    def eliminar_jugador_por_joy(self, instance_id):
        self.jugadores = [j for j in self.jugadores if j.get("instance_id") != instance_id]
        self.reordenar_jugadores()  # Esencial para reasignar "J1", "J2", etc.


    def eliminar_teclado(self):
        self.jugadores = [j for j in self.jugadores if j["tipo"] != "teclado"]
        self.reordenar_jugadores()

    def reordenar_jugadores(self):
        # Simplemente reordena la lista sin huecos y mantiene hasta 4 jugadores
        self.jugadores = self.jugadores[:self.max_jugadores]
        for i, jugador in enumerate(self.jugadores):
            jugador["id_jugador"] = f"J{i + 1}"


gestor_jugadores = GestorJugadores()
