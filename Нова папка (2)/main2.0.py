import pygame as pg
import sys
import random

# Ініціалізація pygame
pg.init()

# Змінні для налаштувань екрану та кольорів
WIDTH = 400
HEIGHT = 400
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
LINE_COLOR = (10, 10, 10)

# Змінні для стану гри
TTT = [0, 0, 0, 0, 0, 0, 0, 0, 0]
winner = None
draw = False

# Налаштування екрану гри
screen = pg.display.set_mode((WIDTH, HEIGHT + 100))
pg.display.set_caption("Tic Tac Toe")

# Завантаження зображень
x_img = pg.image.load("C:\Users\Vitalii\Desktop\Нова папка (2)\x.png")
o_img = pg.image.load("C:\Users\Vitalii\Desktop\Нова папка (2)\o.png")
opening = pg.image.load('tic tac opening.png')

# Масштабування зображень
x_img = pg.transform.scale(x_img, (80, 80))
o_img = pg.transform.scale(o_img, (80, 80))
opening = pg.transform.scale(opening, (WIDTH, HEIGHT + 100))

# Функція для виведення повідомлення про виграш або нічию
def game_status():
    global winner, draw
    if winner:
        if winner == -1:
            print("You won!")
        else:
            print("You lost.")
    elif draw:
        print("It's a draw.")
    else:
        print("Keep playing...")

# Функція для очищення дошки та змінних гри для нової гри
def reset_game():
    global TTT, winner, draw
    TTT = [0, 0, 0, 0, 0, 0, 0, 0, 0]
    winner = None
    draw = False

# Функція для обробки клацання мишею користувача
def user_click():
    global move
    move = None
    x, y = pg.mouse.get_pos()
    if (y < HEIGHT / 3) and (x < WIDTH / 3):
        move = 0
    elif (y < HEIGHT / 3) and (x < WIDTH / 3 * 2):
        move = 1
    elif (y < HEIGHT / 3) and (x < WIDTH):
        move = 2
    elif (y < HEIGHT / 3 * 2) and (x < WIDTH / 3):
        move = 3
    elif (y < HEIGHT / 3 * 2) and (x < WIDTH / 3 * 2):
        move = 4
    elif (y < HEIGHT / 3 * 2) and (x < WIDTH):
        move = 5
    elif (y < HEIGHT) and (x < WIDTH / 3):
        move = 6
    elif (y < HEIGHT) and (x < WIDTH / 3 * 2):
        move = 7
    elif (y < HEIGHT) and (x < WIDTH):
        move = 8

# Головний цикл гри
def X_player():
    global TTT, move, winner, draw
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()

            if event.type == pg.MOUSEBUTTONDOWN:
                user_click()
                if move is not None and TTT[move] == 0:
                    TTT[move] = -1
                    DrawXO()
                    check_win()

        if winner or draw:
            reset_game()
        pg.display.update()

# Перевірка умов перемоги
def check_win():
    global TTT, winner, draw
    for row in range(0, 7, 3):
        if (TTT[row] == TTT[row + 1] == TTT[row + 2]) and (TTT[row] != 0):
            winner = TTT[row]
            pg.draw.line(screen, RED, (0, (row/3 + 1) * HEIGHT / 3 - HEIGHT / 6),
                         (WIDTH, (row/3 + 1) * HEIGHT / 3 - HEIGHT / 6), 6)
            break

    for col in range(0, 3, 1):
        if (TTT[col] == TTT[col + 3] == TTT[col + 6]) and (TTT[col] != 0):
            winner = TTT[col]
            pg.draw.line(screen, RED, ((col + 1) * WIDTH / 3 - WIDTH / 6, 0),
                         ((col + 1) * WIDTH / 3 - WIDTH / 6, HEIGHT), 6)
            break

    if (TTT[0] == TTT[4] == TTT[8]) and (TTT[0] != 0):
        winner = TTT[0]
        pg.draw.line(screen, RED, (50, 50), (350, 350), 6)

    if (TTT[2] == TTT[4] == TTT[6]) and (TTT[2] != 0):
        winner = TTT[2]
        pg.draw.line(screen, RED, (350, 50), (50, 350), 6)

    if TTT.count(0) == 0 and winner is None:
        draw = True
    game_status()

# Функція для малювання Х або О на екрані
def DrawXO():
    global TTT, move
    if move == 0:
        posx = 30
        posy = 30
    elif move == 1:
        posx = WIDTH / 3 + 30
        posy = 30
    elif move == 2:
        posx = WIDTH / 3 * 2 + 30
        posy = 30
    elif move == 3:
        posx = 30
        posy = HEIGHT / 3 + 30
    elif move == 4:
        posx = WIDTH / 3 + 30
        posy = HEIGHT / 3 + 30
    elif move == 5:
        posx = WIDTH / 3 * 2 + 30
        posy = HEIGHT / 3 + 30
    elif move == 6:
        posx = 30
        posy = HEIGHT / 3 * 2 + 30
    elif move == 7:
        posx = WIDTH / 3 + 30
        posy = HEIGHT / 3 * 2 + 30
    elif move == 8:
        posx = WIDTH / 3 * 2 + 30
        posy = HEIGHT / 3 * 2 + 30

    if TTT[move] == -1:
        screen.blit(x_img, (posx, posy))
    else:
        screen.blit(o_img, (posx, posy))

# Головна функція для запуску гри
def main():
    X_player()

if __name__ == "__main__":
    main()
