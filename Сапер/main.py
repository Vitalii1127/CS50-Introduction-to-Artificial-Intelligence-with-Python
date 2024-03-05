import pygame
import random

# Розміри гри
GRID_SIZE = 10
CELL_SIZE = 40
WINDOW_SIZE = GRID_SIZE * CELL_SIZE

# Кількість мін
NUM_MINES = 10

# Колір
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

# Ініціалізація pygame
pygame.init()
screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))

# Створення сітки з мінами
mines = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
revealed = [[False for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
flags = [[False for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]

# Розміщення мін
for _ in range(NUM_MINES):
    while True:
        x = random.randint(0, GRID_SIZE - 1)
        y = random.randint(0, GRID_SIZE - 1)
        if mines[y][x] == 0:
            mines[y][x] = 1
            break

# Змінні для відстеження стану гри
game_over = False
win = False
mines_left = NUM_MINES # Кількість мін, які не позначені прапорцями

# Головний цикл гри
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and not game_over and not win:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            grid_x, grid_y = mouse_x // CELL_SIZE, mouse_y // CELL_SIZE
            # Ліва кнопка миші відкриває клітинку
            if event.button == 1:
                revealed[grid_y][grid_x] = True
                # Якщо клітинка містить міну, гра закінчується
                if mines[grid_y][grid_x] == 1:
                    game_over = True
            # Права кнопка миші ставить прапорець
            elif event.button == 3:
                flags[grid_y][grid_x] = not flags[grid_y][grid_x]
                # Якщо прапорець ставиться, кількість мін зменшується
                if flags[grid_y][grid_x]:
                    mines_left -= 1
                # Якщо прапорець знімається, кількість мін збільшується
                else:
                    mines_left += 1

    screen.fill(WHITE)

    # Відображення сітки
    for x in range(0, WINDOW_SIZE, CELL_SIZE):
        for y in range(0, WINDOW_SIZE, CELL_SIZE):
            rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen, BLACK, rect, 1)

            # Відображення мін
            if revealed[y//CELL_SIZE][x//CELL_SIZE]:
                if mines[y//CELL_SIZE][x//CELL_SIZE] == 1:
                    pygame.draw.circle(screen, RED, (x+CELL_SIZE//2, y+CELL_SIZE//2), CELL_SIZE//4)
            # Відображення прапорців
            elif flags[y//CELL_SIZE][x//CELL_SIZE]:
                pygame.draw.rect(screen, BLUE, rect)

    # Перевірка, чи відкриті всі безпечні клітинки
    safe_cells = GRID_SIZE * GRID_SIZE - NUM_MINES
    revealed_cells = sum(sum(row) for row in revealed)
    if revealed_cells == safe_cells:
        win = True

    # Відображення повідомлення про завершення гри
    if game_over:
        font = pygame.font.SysFont('Arial', 32)
        text = font.render('Game Over', True, BLACK)
        text_rect = text.get_rect()
        text_rect.center = (WINDOW_SIZE//2, WINDOW_SIZE//2)
        screen.blit(text, text_rect)
    elif win:
        font = pygame.font.SysFont('Arial', 32)
        text = font.render('You Win', True, GREEN)
        text_rect = text.get_rect()
        text_rect.center = (WINDOW_SIZE//2, WINDOW_SIZE//2)
        screen.blit(text, text_rect)

    # Відображення кількості мін, які залишилися
    font = pygame.font.SysFont('Arial', 16)
    text = font.render(f'Mines left: {mines_left}', True, BLACK)
    text_rect = text.get_rect()
    text_rect.topleft = (10, 10)
    screen.blit(text, text_rect)

    pygame.display.flip()

pygame.quit()
