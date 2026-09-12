import pygame
import sys
import random
import torch
from model import QNetwork

CELL_SIZE = 20
GRID_WIDTH = 20
GRID_HEIGHT = 20
WINDOW_WIDTH = CELL_SIZE * GRID_WIDTH
WINDOW_HEIGHT = CELL_SIZE * GRID_HEIGHT
FPS = 10

pygame.init()
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 48)

model = QNetwork()
model.load_state_dict(torch.load('model.pth'))
model.eval()

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

def is_collision(point):
    x, y = point
    if x < 0 or x >= GRID_WIDTH or y < 0 or y >= GRID_HEIGHT:
        return True
    if point in snake:
        return True
    return False

def get_state():
    head_x, head_y = snake[0]

    point_l = (head_x - 1, head_y)
    point_r = (head_x + 1, head_y)
    point_u = (head_x, head_y - 1)
    point_d = (head_x, head_y + 1)

    dir_l = direction == (-1, 0)
    dir_r = direction == (1, 0)
    dir_u = direction == (0, -1)
    dir_d = direction == (0, 1)

    state = [
        (dir_r and is_collision(point_r)) or
        (dir_l and is_collision(point_l)) or
        (dir_u and is_collision(point_u)) or
        (dir_d and is_collision(point_d)),

        (dir_u and is_collision(point_r)) or
        (dir_d and is_collision(point_l)) or
        (dir_l and is_collision(point_u)) or
        (dir_r and is_collision(point_d)),

        (dir_d and is_collision(point_r)) or
        (dir_u and is_collision(point_l)) or
        (dir_r and is_collision(point_u)) or
        (dir_l and is_collision(point_d)),

        dir_l, dir_r, dir_u, dir_d,

        food[0] < head_x,
        food[0] > head_x,
        food[1] < head_y,
        food[1] > head_y,
    ]
    return [int(x) for x in state]

def get_ai_action():
    state = get_state()
    state_tensor = torch.tensor(state, dtype=torch.float32)
    prediction = model(state_tensor)
    return torch.argmax(prediction).item()

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
            if game_over and event.key == pygame.K_r:
                reset()
                game_over = False

    if not game_over:
        action = get_ai_action()

        clockwise = [(1, 0), (0, 1), (-1, 0), (0, -1)]
        idx = clockwise.index(direction)

        if action == 0:
            direction = clockwise[idx]
        elif action == 1:
            direction = clockwise[(idx + 1) % 4]
        else:
            direction = clockwise[(idx - 1) % 4]

        head_x, head_y = snake[0]
        dx, dy = direction
        new_head = (head_x + dx, head_y + dy)

        if is_collision(new_head):
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