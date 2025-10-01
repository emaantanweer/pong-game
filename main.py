import pygame
import random
import os

# Constants
SCREEN_WIDTH = 960
SCREEN_HEIGHT = 720
COLOR_BLACK = (0, 0, 0)
COLOR_WHITE = (255, 255, 255)
PADDLE_WIDTH = 7
PADDLE_HEIGHT = 100
BALL_SIZE = 25
PADDLE_SPEED = 0.5

def load_sound(name):
    try:
        return pygame.mixer.Sound(os.path.join(os.path.dirname(__file__), name))
    except Exception as e:
        print(f"Error loading sound {name}: {e}")
        return None


def reset_ball(ball_rect, ball_speed):
    ball_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
    ball_speed[0] = random.choice([-1, 1]) * random.uniform(0.2, 0.4)
    ball_speed[1] = random.choice([-1, 1]) * random.uniform(0.2, 0.4)

def draw_center_text(screen, text, font, color, y_offset=0):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + y_offset))
    screen.blit(text_surface, text_rect)

def main():
    pygame.init()
    pygame.mixer.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('Pong')
    clock = pygame.time.Clock()
    font = pygame.font.SysFont('Consolas', 36)
    small_font = pygame.font.SysFont('Consolas', 24)

    # Load sound
    bounce_sound = load_sound('bounce.wav')

    # Game objects
    paddle_1 = pygame.Rect(30, SCREEN_HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
    paddle_2 = pygame.Rect(SCREEN_WIDTH - 50, SCREEN_HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
    ball = pygame.Rect(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, BALL_SIZE, BALL_SIZE)
    ball_speed = [0, 0]
    reset_ball(ball, ball_speed)

    paddle_1_move = 0
    paddle_2_move = 0

    score = [0, 0]
    started = False
    game_over = False
    winner = None

    while True:
        screen.fill(COLOR_BLACK)

        # Draw scores
        score_text = font.render(f"{score[0]}   {score[1]}", True, COLOR_WHITE)
        screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, 30))

        # Start or restart screen
        if not started:
            draw_center_text(screen, "Press Space to Start", font, COLOR_WHITE)
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    started = True
                    game_over = False
                    winner = None
                    reset_ball(ball, ball_speed)
            clock.tick(60)
            continue

        # Game over screen
        if game_over:
            draw_center_text(screen, f"Player {winner} Wins!", font, COLOR_WHITE, -40)
            draw_center_text(screen, "Press Space to Try Again", small_font, COLOR_WHITE, 40)
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    started = False
                    paddle_1.centery = SCREEN_HEIGHT // 2
                    paddle_2.centery = SCREEN_HEIGHT // 2
                    score = [0, 0]
            clock.tick(60)
            continue

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    paddle_1_move = -PADDLE_SPEED
                if event.key == pygame.K_s:
                    paddle_1_move = PADDLE_SPEED
                if event.key == pygame.K_UP:
                    paddle_2_move = -PADDLE_SPEED
                if event.key == pygame.K_DOWN:
                    paddle_2_move = PADDLE_SPEED
            if event.type == pygame.KEYUP:
                if event.key in (pygame.K_w, pygame.K_s):
                    paddle_1_move = 0
                if event.key in (pygame.K_UP, pygame.K_DOWN):
                    paddle_2_move = 0

        delta_time = clock.tick(60)

        # Move paddles
        paddle_1.y += paddle_1_move * delta_time
        paddle_2.y += paddle_2_move * delta_time
        paddle_1.y = max(0, min(SCREEN_HEIGHT - PADDLE_HEIGHT, paddle_1.y))
        paddle_2.y = max(0, min(SCREEN_HEIGHT - PADDLE_HEIGHT, paddle_2.y))

        # Move ball
        ball.x += ball_speed[0] * delta_time
        ball.y += ball_speed[1] * delta_time

        # Ball collision with top/bottom
        if ball.top <= 0 or ball.bottom >= SCREEN_HEIGHT:
            ball_speed[1] *= -1
            if bounce_sound: bounce_sound.play()

        # Ball collision with paddles
        if ball.colliderect(paddle_1) and ball_speed[0] < 0:
            ball_speed[0] *= -1.1  # Increase speed for fun
            ball.x = paddle_1.right
            if bounce_sound: bounce_sound.play()
        if ball.colliderect(paddle_2) and ball_speed[0] > 0:
            ball_speed[0] *= -1.1
            ball.x = paddle_2.left - BALL_SIZE
            if bounce_sound: bounce_sound.play()

        # Score and reset
        if ball.left <= 0:
            score[1] += 1
            if score[1] >= 5:
                game_over = True
                winner = 2
            else:
                reset_ball(ball, ball_speed)
        if ball.right >= SCREEN_WIDTH:
            score[0] += 1
            if score[0] >= 5:
                game_over = True
                winner = 1
            else:
                reset_ball(ball, ball_speed)

        # Draw paddles and ball
        pygame.draw.rect(screen, COLOR_WHITE, paddle_1)
        pygame.draw.rect(screen, COLOR_WHITE, paddle_2)
        pygame.draw.ellipse(screen, COLOR_WHITE, ball)

        # Draw center line
        for y in range(0, SCREEN_HEIGHT, 40):
            pygame.draw.rect(screen, COLOR_WHITE, (SCREEN_WIDTH // 2 - 2, y, 4, 20))

        pygame.display.flip()

if __name__ == '__main__':
    main()