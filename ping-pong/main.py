import pygame
import sys

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

def draw_ball(ball_pos):
    pygame.draw.circle(screen, WHITE, ball_pos, BALL_RADIUS)

def draw_paddle1(paddle1_pos):
    pygame.draw.rect(screen, WHITE, pygame.Rect((0, paddle1_pos), (PADDLE_WIDTH, PADDLE_HEIGHT)))

def draw_paddle2(paddle2_pos):
    pygame.draw.rect(screen, WHITE, pygame.Rect((WIDTH - PADDLE_WIDTH, paddle2_pos), (PADDLE_WIDTH, PADDLE_HEIGHT)))

def ai(paddle2_pos, ball_pos, ball_vel):
    # Прогнозуємо, де м'яч приземлиться
    future_ball_pos = ball_pos[1] + ball_vel[1]
    if future_ball_pos < 0:
        future_ball_pos = -future_ball_pos
    elif future_ball_pos > HEIGHT:
        future_ball_pos = HEIGHT - (future_ball_pos - HEIGHT)

    if paddle2_pos < future_ball_pos:
        paddle2_pos += 2
    if paddle2_pos > future_ball_pos:
        paddle2_pos -= 2
    return paddle2_pos

def game(difficulty):
    ball_pos = [0, 0]
    ball_vel = [0, 0]
    paddle1_vel = 0
    paddle2_vel = 0
    paddle1_pos = HEIGHT // 2
    paddle2_pos = HEIGHT // 2
    score1 = 0
    score2 = 0

    # Встановлюємо швидкість м'яча та платформи в залежності від обраного рівня складності
    if difficulty == 'easy':
        ball_vel = [2, 2]
        PADDLE_SPEED = 2
    elif difficulty == 'medium':
        ball_vel = [3, 3]
        PADDLE_SPEED = 3
    elif difficulty == 'hard':
        ball_vel = [4, 4]
        PADDLE_SPEED = 4

    ball_pos = [WIDTH // 2, HEIGHT // 2]

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
        paddle2_pos = ai(paddle2_pos, ball_pos, ball_vel)

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
        elif ball_pos[0] >= WIDTH - BALL_RADIUS - PADDLE_WIDTH:
            ball_pos = [WIDTH // 2, HEIGHT // 2]
            ball_vel = [-ball_vel[0], ball_vel[1]]
            score1 += 1

        if ball_pos[1] <= BALL_RADIUS or ball_pos[1] >= HEIGHT - BALL_RADIUS:
            ball_vel[1] = -ball_vel[1] * SPEED_INCREASE_FACTOR
            if abs(ball_vel[1]) > MAX_BALL_SPEED:
                ball_vel[1] = MAX_BALL_SPEED if ball_vel[1] > 0 else -MAX_BALL_SPEED

        score_text = font.render(f"Player 1: {score1}   Player 2: {score2}", True, WHITE)
        screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, 5))

        pygame.display.update()
        clock.tick(FPS)

def main_menu():
    title_font = pygame.font.Font(None, 50)
    button_font = pygame.font.Font(None, 36)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.fill(BLACK)
        title_text = title_font.render("Виберіть рівень складності", True, WHITE)
        screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, 20))  # Зменшено відстань

        mx, my = pygame.mouse.get_pos()

        button_width = 200
        button_height = 50
        easy_button = pygame.Rect(WIDTH // 2 - button_width // 2, 100, button_width, button_height)  # Зменшено відстань
        medium_button = pygame.Rect(WIDTH // 2 - button_width // 2, 200, button_width, button_height)
        hard_button = pygame.Rect(WIDTH // 2 - button_width // 2, 300, button_width, button_height)

        if easy_button.collidepoint((mx, my)):
            if pygame.mouse.get_pressed()[0]:
                game('easy')
        if medium_button.collidepoint((mx, my)):
            if pygame.mouse.get_pressed()[0]:
                game('medium')
        if hard_button.collidepoint((mx, my)):
            if pygame.mouse.get_pressed()[0]:
                game('hard')

        pygame.draw.rect(screen, WHITE, easy_button)
        pygame.draw.rect(screen, WHITE, medium_button)
        pygame.draw.rect(screen, WHITE, hard_button)

        easy_text = button_font.render("Легко", True, BLACK)
        screen.blit(easy_text, (WIDTH // 2 - easy_text.get_width() // 2, 115))  # Зменшено відстань
        medium_text = button_font.render("Середньо", True, BLACK)
        screen.blit(medium_text, (WIDTH // 2 - medium_text.get_width() // 2, 215))
        hard_text = button_font.render("Важко", True, BLACK)
        screen.blit(hard_text, (WIDTH // 2 - hard_text.get_width() // 2, 315))

        pygame.display.update()
        clock.tick(FPS)

if __name__ == '__main__':
    main_menu()
