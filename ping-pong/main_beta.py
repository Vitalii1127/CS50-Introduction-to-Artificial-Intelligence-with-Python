import pygame
import sys
import numpy as np

# Глобальні константи
WIDTH, HEIGHT = 600, 400
BALL_RADIUS = 10
PADDLE_WIDTH, PADDLE_HEIGHT = 15, 80
FPS = 60
PADDLE_SPEED = 2
SPEED_INCREASE_FACTOR = 1.03  # Множник для збільшення швидкості м'яча зменшено на 70%
MAX_BALL_SPEED = 4  # Максимальна швидкість м'яча

# Кольори
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Ініціалізація Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)

# Ініціалізація Q-таблиці
Q = np.zeros((HEIGHT // BALL_RADIUS, HEIGHT // BALL_RADIUS, 2))

def draw_ball(ball_pos):
    pygame.draw.circle(screen, WHITE, ball_pos, BALL_RADIUS)

def draw_paddle1(paddle1_pos):
    pygame.draw.rect(screen, WHITE, pygame.Rect((0, paddle1_pos), (PADDLE_WIDTH, PADDLE_HEIGHT)))

def draw_paddle2(paddle2_pos):
    pygame.draw.rect(screen, WHITE, pygame.Rect((WIDTH - PADDLE_WIDTH, paddle2_pos), (PADDLE_WIDTH, PADDLE_HEIGHT)))

def ai(paddle2_pos, ball_pos, ball_vel):
    # Використовуємо Q-таблицю для вибору дії
    state = (max(0, int(ball_pos[1] // BALL_RADIUS)), max(0, int(paddle2_pos // BALL_RADIUS)))  # Додано перевірку
    action = np.argmax(Q[state])
    if action == 0:
        paddle2_pos -= PADDLE_SPEED
    else:
        paddle2_pos += PADDLE_SPEED
    return paddle2_pos, action  # Повертаємо дію

def update_q_table(paddle2_pos, ball_pos, reward, action):
    # Оновлюємо Q-таблицю використовуючи формулу Q-навчання
    state = (max(0, int(ball_pos[1] // BALL_RADIUS)), max(0, int(paddle2_pos // BALL_RADIUS)))  # Додано перевірку
    Q[state][action] = Q[state][action] + 0.1 * (reward + 0.95 * np.max(Q[state]) - Q[state][action])

def game():
    ball_pos = [0, 0]
    ball_vel = [0, 0]
    paddle1_vel = 0
    paddle2_vel = 0
    paddle1_pos = HEIGHT // 2
    paddle2_pos = HEIGHT // 2
    score1 = 0
    score2 = 0

    ball_pos = [WIDTH // 2, HEIGHT // 2]
    ball_vel = [2, 2]

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            paddle1_pos -= PADDLE_SPEED
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            paddle1_pos += PADDLE_SPEED

        screen.fill(BLACK)
        draw_ball(ball_pos)
        draw_paddle1(paddle1_pos)
        draw_paddle2(paddle2_pos)

        ball_pos[0] += ball_vel[0]
        ball_pos[1] += ball_vel[1]

        paddle1_pos += paddle1_vel
        paddle2_pos, action = ai(paddle2_pos, ball_pos, ball_vel)  # Отримуємо дію

        if ball_pos[0] <= BALL_RADIUS + PADDLE_WIDTH and paddle1_pos < ball_pos[1] < paddle1_pos + PADDLE_HEIGHT:
            ball_vel[0] = -ball_vel[0] * SPEED_INCREASE_FACTOR
            if abs(ball_vel[0]) > MAX_BALL_SPEED:
                ball_vel[0] = MAX_BALL_SPEED if ball_vel[0] > 0 else -MAX_BALL_SPEED
        elif ball_pos[0] >= WIDTH - BALL_RADIUS - PADDLE_WIDTH and paddle2_pos < ball_pos[1] < paddle2_pos + PADDLE_HEIGHT:
            ball_vel[0] = -ball_vel[0] * SPEED_INCREASE_FACTOR
            if abs(ball_vel[0]) > MAX_BALL_SPEED:
                ball_vel[0] = MAX_BALL_SPEED if ball_vel[0] > 0 else -MAX_BALL_SPEED
        elif ball_pos[0] <= BALL_RADIUS + PADDLE_WIDTH:
            ball_pos = [WIDTH // 2, HEIGHT // 2]
            ball_vel = [-ball_vel[0], ball_vel[1]]
            score2 += 1
            update_q_table(paddle2_pos, ball_pos, -1, action)
        elif ball_pos[0] >= WIDTH - BALL_RADIUS - PADDLE_WIDTH:
            ball_pos = [WIDTH // 2, HEIGHT // 2]
            ball_vel = [-ball_vel[0], ball_vel[1]]
            score1 += 1
            update_q_table(paddle2_pos, ball_pos, 1, action)

        if ball_pos[1] <= BALL_RADIUS or ball_pos[1] >= HEIGHT - BALL_RADIUS:
            ball_vel[1] = -ball_vel[1] * SPEED_INCREASE_FACTOR
            if abs(ball_vel[1]) > MAX_BALL_SPEED:
                ball_vel[1] = MAX_BALL_SPEED if ball_vel[1] > 0 else -MAX_BALL_SPEED

        score_text = font.render(f"Player 1: {score1}   Player 2: {score2}", True, WHITE)
        screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, 5))

        pygame.display.update()
        clock.tick(FPS)

if __name__ == '__main__':
    game()
