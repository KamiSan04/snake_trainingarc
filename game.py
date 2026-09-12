import pygame
import sys
import random

CELL_SIZE = 20
GRID_WIDTH = 20
GRID_HEIGHT = 20
WINDOW_WIDTH = CELL_SIZE * GRID_WIDTH
WINDOW_HEIGHT = CELL_SIZE * GRID_HEIGHT
FPS = 5

pygame.init()
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 48)

def reset():
    global snake, direction, food
    snake = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
    direction = (1, 0)
    food = spawn_food()

def spawn_food():
    while True:
        pos = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
        if pos not in snake:
            return pos

def draw(game_over):
    screen.fill((0, 0, 0))
    for segment in snake:
        x, y = segment
        rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(screen, (0, 255, 0), rect)
    fx, fy = food
    food_rect = pygame.Rect(fx * CELL_SIZE, fy * CELL_SIZE, CELL_SIZE, CELL_SIZE)
    pygame.draw.rect(screen, (255, 0, 0), food_rect)

    if game_over:
        text = font.render("GAME OVER - press R", True, (255, 255, 255))
        rect = text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
        screen.blit(text, rect)

    pygame.display.flip()

snake = None
direction = None
food = None
reset()
game_over = False

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if game_over:
                if event.key == pygame.K_r:
                    reset()
                    game_over = False
            else:
                if event.key == pygame.K_UP and direction != (0, 1):
                    direction = (0, -1)
                elif event.key == pygame.K_DOWN and direction != (0, -1):
                    direction = (0, 1)
                elif event.key == pygame.K_LEFT and direction != (1, 0):
                    direction = (-1, 0)
                elif event.key == pygame.K_RIGHT and direction != (-1, 0):
                    direction = (1, 0)

    if not game_over:
        head_x, head_y = snake[0]
        dx, dy = direction
        new_head = (head_x + dx, head_y + dy)

        hit_wall = (
            new_head[0] < 0 or new_head[0] >= GRID_WIDTH or
            new_head[1] < 0 or new_head[1] >= GRID_HEIGHT
        )
        hit_self = new_head in snake

        if hit_wall or hit_self:
            game_over = True
        else:
            snake.insert(0, new_head)
            if new_head == food:
                food = spawn_food()
            else:
                snake.pop()

    draw(game_over)
    clock.tick(FPS)

pygame.quit()
sys.exit()