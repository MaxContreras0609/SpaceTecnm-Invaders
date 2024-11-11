import pygame
import random
import math

# Inicializar pygame
pygame.init()

# Configuración de la pantalla
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('ufo.png')  # Ícono de la ventana
icon = pygame.transform.scale(icon, (100, 100))  # Redimensionamos el ícono del UFO
pygame.display.set_icon(icon)

# Fondo
background = pygame.image.load('background.png')
background = pygame.transform.scale(background, (800, 600))  # Ajustamos el fondo a 800x600

# Jugador
player_image = pygame.image.load('player.png')
player_image = pygame.transform.scale(player_image, (60, 60))  # Redimensionamos el jugador a 60x60
player_x = 370
player_y = 480
player_x_change = 0
player_speed = 1  # Reducir la velocidad del jugador

# Enemigos
enemy_image = []
enemy_x = []
enemy_y = []
enemy_x_change = []
enemy_y_change = []
num_of_enemies = 2
enemy_speed = 0.7  # Reducir la velocidad de los enemigos

for i in range(num_of_enemies):
    enemy_image.append(pygame.image.load('enemy.png'))
    enemy_image[i] = pygame.transform.scale(enemy_image[i], (60, 60))  # Redimensionamos los enemigos a 60x60
    enemy_x.append(random.randint(0, 735))
    enemy_y.append(random.randint(50, 150))
    enemy_x_change.append(enemy_speed)
    enemy_y_change.append(40)

# Proyectil
bullet_image = pygame.image.load('bullet.png')
bullet_image = pygame.transform.scale(bullet_image, (40, 30))  # Redimensionamos la bala a 40x30
bullet_x = 0
bullet_y = 480
bullet_y_change = 2  # Reducir la velocidad de la bala
bullet_state = "ready"  # "ready" significa que no se muestra en pantalla

# Puntuación
score = 0
font = pygame.font.Font('freesansbold.ttf', 32)
text_x = 10
text_y = 10

# Función para mostrar la puntuación
def show_score(x, y):
    score_value = font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(score_value, (x, y))

# Función para dibujar al jugador
def player(x, y):
    screen.blit(player_image, (x, y))

# Función para dibujar al enemigo
def enemy(x, y, i):
    screen.blit(enemy_image[i], (x, y))

# Función para disparar la bala
def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bullet_image, (x + 16, y + 10))

# Función para detectar colisiones
def is_collision(enemy_x, enemy_y, bullet_x, bullet_y):
    distance = math.sqrt((math.pow(enemy_x - bullet_x, 2)) + (math.pow(enemy_y - bullet_y, 2)))
    return distance < 27

# Bucle principal del juego
running = True
while running:
    screen.fill((0, 0, 0))  # Fondo negro
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Comprobar si se presionó una tecla
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player_x_change = -player_speed
            if event.key == pygame.K_RIGHT:
                player_x_change = player_speed
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bullet_x = player_x
                    fire_bullet(bullet_x, bullet_y)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                player_x_change = 0

    # Actualizar la posición del jugador
    player_x += player_x_change
    player_x = max(0, min(player_x, 736))

    # Movimiento del enemigo
    for i in range(num_of_enemies):
        enemy_x[i] += enemy_x_change[i]
        if enemy_x[i] <= 0:
            enemy_x_change[i] = enemy_speed
            enemy_y[i] += enemy_y_change[i]
        elif enemy_x[i] >= 736:
            enemy_x_change[i] = -enemy_speed
            enemy_y[i] += enemy_y_change[i]

        # Comprobar colisiones
        collision = is_collision(enemy_x[i], enemy_y[i], bullet_x, bullet_y)
        if collision:
            bullet_y = 480
            bullet_state = "ready"
            score += 1
            enemy_x[i] = random.randint(0, 735)
            enemy_y[i] = random.randint(50, 150)

        enemy(enemy_x[i], enemy_y[i], i)

    # Movimiento de la bala
    if bullet_state == "fire":
        fire_bullet(bullet_x, bullet_y)
        bullet_y -= bullet_y_change

    if bullet_y <= 0:
        bullet_y = 480
        bullet_state = "ready"

    player(player_x, player_y)
    show_score(text_x, text_y)
    pygame.display.update()
