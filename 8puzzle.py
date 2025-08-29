import pygame
import sys
import random

#Khởi tạo
pygame.init()
TILE_SIZE = 100
GRID_SIZE = 3
WIDTH = HEIGHT = TILE_SIZE * GRID_SIZE
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE  = (50, 100, 200)
font = pygame.font.SysFont("Arial", 40)
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("8 Puzzle Game")

#Tạo một mảng số ngẫu nhiên để người chơi giải
tiles = list(range(1, 9)) + [0]
random.shuffle(tiles)

#Tạo ma trận
def get_grid(tiles):
    grid = []
    for i in range(0, len(tiles), GRID_SIZE):
        grid.append(tiles[i:i+GRID_SIZE])
    return grid
def draw_grid(tiles):
    grid = get_grid(tiles)
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            value = grid[i][j]
            rect = pygame.Rect(j*TILE_SIZE, i*TILE_SIZE, TILE_SIZE, TILE_SIZE)
            pygame.draw.rect(screen, BLACK, rect, 2)
            if value != 0:
                pygame.draw.rect(screen, BLUE, rect)
                text = font.render(str(value), True, WHITE)
                text_rect = text.get_rect(center=rect.center)
                screen.blit(text, text_rect)

#Tìm 0
def find_zero(tiles):
    for i in range(len(tiles)):
        if tiles[i] == 0:
            row = i // GRID_SIZE
            col = i % GRID_SIZE
            return row, col

#Di chuyển
def move(tiles, dx, dy):
    x, y = find_zero(tiles)
    nx, ny = x + dx, y + dy
    if 0 <= nx < GRID_SIZE and 0 <= ny < GRID_SIZE:
        idx1 = x * GRID_SIZE + y
        idx2 = nx * GRID_SIZE + ny
        tiles[idx1], tiles[idx2] = tiles[idx2], tiles[idx1]

goal = list(range(1, 9)) + [0] #Kết quả

#Cơ chế game
running = True
while running:
    screen.fill(WHITE)
    draw_grid(tiles)
    if tiles == goal:
        text = font.render("YOU WIN!", True, (200,0,0))
        screen.blit(text, (90, 130))
    pygame.display.flip()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                move(tiles, 1, 0)
            elif event.key == pygame.K_DOWN:
                move(tiles, -1, 0)
            elif event.key == pygame.K_LEFT:
                move(tiles, 0, 1)
            elif event.key == pygame.K_RIGHT:
                move(tiles, 0, -1)