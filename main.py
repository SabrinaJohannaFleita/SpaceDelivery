import pygame
import sys
import random

# 1. SETUP INITIAL (Aula 1 & 2)
pygame.init()

SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Space Delivery: Mission Orbit")

# Background
try:
    bg_image = pygame.image.load("background.png")
    bg_image = pygame.transform.scale(bg_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
    player_img = pygame.image.load("ship.png")
    asteroid_img = pygame.image.load("asteroid.png")
    package_img = pygame.image.load("package.png")
    # Sound
    laser_sound = pygame.mixer.Sound("laser.wav")
    explosion_sound = pygame.mixer.Sound("explosion.wav")

    # Music
    pygame.mixer.music.load("background_music.wav")
    pygame.mixer.music.set_volume(0.3)  # Volumen 30%
    pygame.mixer.music.play(-1)  # Infinite
except pygame.error as e:
    print(f"Error: No se pudo cargar background.png. Asegúrate de que el archivo esté en la misma carpeta. Detalle: {e}")
    sys.exit()


# Colors
BLACK = (10, 10, 20)
WHITE = (255, 255, 255)
NEON_GREEN = (57, 255, 20)
BLUE = (50, 150, 255)
RED = (255, 50, 50)
YELLOW = (255, 255, 0)

# Fonts
title_font = pygame.font.SysFont("Arial", 50, bold=True)
text_font = pygame.font.SysFont("Arial", 24)


# 2. PLAYER CLASS
class Player:
    def __init__(self):
        self.width = 110
        self.height = 60
        self.x = SCREEN_WIDTH // 2 - self.width // 2
        self.y = SCREEN_HEIGHT - 70
        self.speed = 7
        self.image = pygame.transform.scale(player_img, (self.width, self.height))

    def move(self, keys):
        if keys[pygame.K_LEFT] and self.x > 0:
            self.x -= self.speed
        if keys[pygame.K_RIGHT] and self.x < SCREEN_WIDTH - self.width:
            self.x += self.speed

    def draw(self, surface):
        surface.blit(self.image, (self.x, self.y))


# 3. ITEM CLASS (Obstáculos y Paquetes - El Desafío y el Objetivo)
class Item:
    def __init__(self, item_type):
        self.item_type = item_type  # Puede ser "obstacle" o "package"
        self.width = 60
        self.height = 60
        self.x = random.randint(0, SCREEN_WIDTH - self.width)
        self.y = -self.height
        self.speed = random.randint(3, 6)

        # Cargamos y escalamos la imagen correspondiente según el tipo de objeto
        if self.item_type == "obstacle":
            self.image = pygame.transform.scale(asteroid_img, (self.width, self.height))
        else:
            self.image = pygame.transform.scale(package_img, (self.width, self.height))

    def update(self):
        self.y += self.speed

    def draw(self, surface):
        surface.blit(self.image, (self.x, self.y))


# FUNCIÓN MENU
def show_menu():
    screen.blit(bg_image, (0, 0))

    # Capa oscura transparente para que resalten las letras
    dark_overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    dark_overlay.fill((0, 0, 0))
    dark_overlay.set_alpha(150)
    screen.blit(dark_overlay, (0, 0))

    # Title
    title_surface = title_font.render("DELIVERY ESPACIAL", True, NEON_GREEN)
    screen.blit(title_surface, (SCREEN_WIDTH // 2 - title_surface.get_width() // 2, 150))

    # UI Requirements (Controles obrigatórios em tela)
    controls_title = text_font.render("CONTROLES DA NAVE:", True, WHITE)
    move_control = text_font.render("<- / -> : Mover Nave de Entrega", True, WHITE)
    action_control = text_font.render("ESPAÇO : Lançar Raio Coletor", True, WHITE)
    start_text = text_font.render("Pressione ENTER para iniciar a entrega", True, NEON_GREEN)

    screen.blit(controls_title, (SCREEN_WIDTH // 2 - controls_title.get_width() // 2, 280))
    screen.blit(move_control, (SCREEN_WIDTH // 2 - move_control.get_width() // 2, 320))
    screen.blit(action_control, (SCREEN_WIDTH // 2 - action_control.get_width() // 2, 350))
    screen.blit(start_text, (SCREEN_WIDTH // 2 - start_text.get_width() // 2, 450))

    pygame.display.flip()


# Game Loop Variables
player = Player()
items = []
spawn_timer = 0
clock = pygame.time.Clock()
is_running = True
in_menu = True

# Game Stats
lives = 3
score = 0
game_over = False
victory = False
laser_active = False
laser_timer = 0

# 4. MAIN GAME LOOP
while is_running:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False

        if in_menu:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    in_menu = False

        elif not game_over and not victory:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not laser_active:
                    laser_active = True
                    laser_timer = 10
                    laser_sound.play()
                    laser_sound.fadeout(300)
    if in_menu:
        show_menu()
    else:
        if not game_over and not victory:
            # CONTROLES DE MOVIMIENTO
            keys_pressed = pygame.key.get_pressed()
            player.move(keys_pressed)

            # APARECER OBSTÁCULOS O PAQUETES
            spawn_timer += 1
            if spawn_timer >= 40:
                tipo = "obstacle" if random.random() < 0.7 else "package"
                items.append(Item(tipo))
                spawn_timer = 0

            # LÓGICA DEL RAYO COLETOR (Fuera del spawn, corre a 60 FPS)
            laser_rect = None
            if laser_active:
                laser_rect = pygame.Rect(player.x + player.width // 2 - 10, 0, 20, player.y)
                laser_timer -= 1
                if laser_timer <= 0:
                    laser_active = False

            # ACTUALIZAR ITEMS Y DETECTAR COLISIONES (Fuera del spawn, corre a 60 FPS)
            for item in items[:]:
                item.update()

                item_rect = pygame.Rect(item.x, item.y, item.width, item.height)
                player_rect = pygame.Rect(player.x, player.y, player.width, player.height)

                # 1. Choque físico con la nave
                if player_rect.colliderect(item_rect):
                    if item.item_type == "obstacle":
                        explosion_sound.play()
                        lives -= 1
                        if lives <= 0:
                            game_over = True
                    items.remove(item)

                # 2. Captura con el Raio Coletor
                elif laser_active and laser_rect and laser_rect.colliderect(item_rect):
                    if item.item_type == "package":
                        score += 1  # Acá suma las entregas perfectamente
                        if score >= 10:
                            victory = True
                    items.remove(item)

            items = [it for it in items if it.y < SCREEN_HEIGHT]

            # DESENHAR TELA DE JOGO
            screen.blit(bg_image, (0, 0))

            if laser_active:
                pygame.draw.rect(screen, YELLOW, (player.x + player.width // 2 - 5, 0, 10, player.y))

            player.draw(screen)
            for item in items:
                item.draw(screen)

            hud_surface = text_font.render(f"Vidas: {lives}   |   Entregas: {score}/10", True, WHITE)
            screen.blit(hud_surface, (20, 20))

        elif game_over:
            screen.blit(bg_image, (0, 0))
            game_over_surface = title_font.render("GAME OVER", True, RED)
            restart_surface = text_font.render("Pressione ENTER para tentar novamente", True, WHITE)
            screen.blit(game_over_surface, (SCREEN_WIDTH // 2 - game_over_surface.get_width() // 2, 250))
            screen.blit(restart_surface, (SCREEN_WIDTH // 2 - restart_surface.get_width() // 2, 330))

            keys = pygame.key.get_pressed()
            if keys[pygame.K_RETURN]:
                lives = 3
                score = 0
                items.clear()
                game_over = False
                player.x = SCREEN_WIDTH // 2 - player.width // 2

        elif victory:
            screen.blit(bg_image, (0, 0))
            win_surface = title_font.render("MISSÃO CONCLUÍDA!", True, NEON_GREEN)
            sub_surface = text_font.render("Parabéns! Todas as entregas foram feitas.", True, WHITE)
            restart_surface = text_font.render("Pressione ENTER para jogar de novo", True, WHITE)

            screen.blit(win_surface, (SCREEN_WIDTH // 2 - win_surface.get_width() // 2, 220))
            screen.blit(sub_surface, (SCREEN_WIDTH // 2 - sub_surface.get_width() // 2, 300))
            screen.blit(restart_surface, (SCREEN_WIDTH // 2 - restart_surface.get_width() // 2, 380))

            keys = pygame.key.get_pressed()
            if keys[pygame.K_RETURN]:
                lives = 3
                score = 0
                items.clear()
                victory = False
                player.x = SCREEN_WIDTH // 2 - player.width // 2

        pygame.display.flip()

pygame.quit()
sys.exit()