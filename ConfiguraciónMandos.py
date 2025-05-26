import pygame

pygame.init()
pygame.joystick.init()

# Lista para guardar mandos que se han unido
mandos_activos = []

# Diccionario para asociar ID de mando con su joystick
mandos_detectados = {}

# Función para escanear y registrar nuevos mandos
def detectar_nuevos_mandos():
    for i in range(pygame.joystick.get_count()):
        if i not in mandos_detectados:
            joystick = pygame.joystick.Joystick(i)
            joystick.init()
            mandos_detectados[i] = joystick
            print(f"🎮 Mando {i} detectado: {joystick.get_name()}")

# Función para procesar si un mando quiere unirse
def procesar_union_mando(event):
    if event.type == pygame.JOYBUTTONDOWN:
        joy_id = event.joy
        if joy_id in mandos_detectados and joy_id not in mandos_activos:
            mandos_activos.append(joy_id)
            print(f"✅ Mando {joy_id} se ha unido al juego")

pantalla = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Pantalla de unión de mandos")
clock = pygame.time.Clock()

detectados_previamente = pygame.joystick.get_count()
detectar_nuevos_mandos()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        procesar_union_mando(event)

    # Revisar si se ha conectado un nuevo mando (hotplug)
    nuevos_detectados = pygame.joystick.get_count()
    if nuevos_detectados > detectados_previamente:
        detectar_nuevos_mandos()
        detectados_previamente = nuevos_detectados

    pantalla.fill((20, 20, 40))
    pygame.display.flip()
    clock.tick(60)

pygame.quit()

