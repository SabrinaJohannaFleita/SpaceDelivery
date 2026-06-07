import pygame
import sys

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


# 2. PLAYER CLASS (Para tu diagrama UML de la Aula 2)
class Player:
    def __init__(self):
        # Usamos un rectángulo simple por ahora para no renegar con imágenes de entrada
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
        # Dibujamos un rectángulo azul que representa nuestra nave espacial
        pygame.draw.rect(surface, BLUE, (self.x, self.y, self.width, self.height))


def show_menu():
    screen.fill(BLACK)

    # Title
    title_surface = title_font.render("DELIVERY ESPACIAL", True, NEON_GREEN)
    screen.blit(title_surface, (SCREEN_WIDTH // 2 - title_surface.get_width() // 2, 150))

    # UI Requirements (Controles obligatorios en pantalla)
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
clock = pygame.time.Clock()
is_running = True
in_menu = True

# 3. MAIN GAME LOOP
while is_running:
    clock.tick(60)  # Capado a 60 FPS para que no vaya a mil por hora

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False

        if in_menu:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:  # ENTER Key para arrancar
                    in_menu = False

    if in_menu:
        show_menu()
    else:
        # CONTROLES (Manejo del teclado para el Player)
        keys_pressed = pygame.key.get_pressed()
        player.move(keys_pressed)

        # DIBUJAR PANTALLA DE JUEGO
        screen.fill((15, 15, 30))  # Fondo del espacio oscuro
        player.draw(screen)  # Dibujamos la nave en su posición actual

        pygame.display.flip()

pygame.quit()
sys.exit()
