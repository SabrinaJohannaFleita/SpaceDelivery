import pygame
import sys
import random

# 1. SETUP INITIAL (Aula 1 & 2)
pygame.init()

SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Space Delivery: Mission Orbit")

# Colors
BLACK = (10, 10, 20)
WHITE = (255, 255, 255)
NEON_GREEN = (57, 255, 20)
BLUE = (50, 150, 255)

# Fonts
title_font = pygame.font.SysFont("Arial", 50, bold=True)
text_font = pygame.font.SysFont("Arial", 24)


# 2. PLAYER CLASS (Aula 2)
class Player:
    def __init__(self):
        self.width = 50
        self.height = 40
        self.x = SCREEN_WIDTH // 2 - self.width // 2
        self.y = SCREEN_HEIGHT - 70
        self.speed = 7

    def move(self, keys):
        if keys[pygame.K_LEFT] and self.x > 0:
            self.x -= self.speed
        if keys[pygame.K_RIGHT] and self.x < SCREEN_WIDTH - self.width:
            self.x += self.speed

    def draw(self, surface):
        pygame.draw.rect(surface, BLUE, (self.x, self.y, self.width, self.height))


# 3. OBSTACLE CLASS (O desafio exigido no PDF)
class Obstacle:
    def __init__(self):
        self.width = 40
        self.height = 40
        self.x = random.randint(0, SCREEN_WIDTH - self.width)
        self.y = -self.height
        self.speed = random.randint(3, 6)

    def update(self):
        self.y += self.speed

    def draw(self, surface):
        pygame.draw.rect(surface, (255, 50, 50), (self.x, self.y, self.width, self.height))


def show_menu():
    screen.fill(BLACK)

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
obstacles = []
spawn_timer = 0
clock = pygame.time.Clock()
is_running = True
in_menu = True
lives = 3  # <-- CONTROL DE VIDAS
game_over = False  # <-- BANDERA DE DERROTA DEFINIDA AQUÍ

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

    if in_menu:
        show_menu()
    else:
        if not game_over:
            # CONTROLES
            keys_pressed = pygame.key.get_pressed()
            player.move(keys_pressed)

            # LOGICA DOS OBSTACULOS
            spawn_timer += 1
            if spawn_timer >= 45:
                obstacles.append(Obstacle())
                spawn_timer = 0

            for obstacle in obstacles[:]:  # Copia de la lista para remover seguro
                obstacle.update()

                # CHEQUEAR COLISIÓN
                player_rect = pygame.Rect(player.x, player.y, player.width, player.height)
                obstacle_rect = pygame.Rect(obstacle.x, obstacle.y, obstacle.width, obstacle.height)

                if player_rect.colliderect(obstacle_rect):
                    lives -= 1
                    obstacles.remove(obstacle)
                    if lives <= 0:
                        game_over = True

            # Limpar obstáculos fora da tela
            obstacles = [obs for obs in obstacles if obs.y < SCREEN_HEIGHT]

            # DESENHAR TELA DE JOGO (NORMAL)
            screen.fill((15, 15, 30))
            player.draw(screen)
            for obstacle in obstacles:
                obstacle.draw(screen)

            # Mostrar vidas en portugués
            lives_surface = text_font.render(f"Vidas: {lives}", True, WHITE)
            screen.blit(lives_surface, (20, 20))

        else:
            # PANTALLA DE GAME OVER
            screen.fill((15, 15, 30))
            game_over_surface = title_font.render("GAME OVER", True, (255, 50, 50))
            restart_surface = text_font.render("Pressione ENTER para tentar novamente", True, WHITE)

            screen.blit(game_over_surface, (SCREEN_WIDTH // 2 - game_over_surface.get_width() // 2, 250))
            screen.blit(restart_surface, (SCREEN_WIDTH // 2 - restart_surface.get_width() // 2, 330))

            # Reiniciar si presiona Enter estando en Game Over
            keys = pygame.key.get_pressed()
            if keys[pygame.K_RETURN]:
                lives = 3
                obstacles.clear()
                game_over = False
                player.x = SCREEN_WIDTH // 2 - player.width // 2

        pygame.display.flip()

pygame.quit()
sys.exit()