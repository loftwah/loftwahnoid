import pygame
import random
from .constants import WIDTH, HEIGHT, FPS, BLACK, WHITE, RED, GREEN, BLUE
from .sprites.paddle import Paddle
from .sprites.ball import Ball
from .sprites.brick import Brick
from .menus import pause_menu

def game_loop(screen):
    clock = pygame.time.Clock()
    paddle_width = 100
    paddle_height = 10
    paddle = Paddle(WIDTH // 2 - paddle_width // 2, HEIGHT - 30, paddle_width, paddle_height, 7)
    ball = Ball(WIDTH // 2, HEIGHT - 50, 8, 5)
    bricks = []
    rows = 5
    cols = 10
    spacing = 5
    brick_width = (WIDTH - (cols + 1) * spacing) / cols
    brick_height = 20

    # Create bricks arranged in rows and columns
    for row in range(rows):
        for col in range(cols):
            x = spacing + col * (brick_width + spacing)
            y = 50 + row * (brick_height + spacing)
            color = random.choice([RED, GREEN, BLUE])
            bricks.append(Brick(x, y, brick_width, brick_height, color))

    running = True
    game_over = False

    while running:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if not pause_menu(screen):
                        running = False
                        return

        keys = pygame.key.get_pressed()
        paddle.update(keys)
        if not game_over:
            ball.update()

        # Ball collision with paddle
        if ball.get_rect().colliderect(paddle.rect):
            ball.vel_y = -abs(ball.vel_y)
            offset = (ball.x - paddle.rect.centerx) / (paddle.rect.width / 2)
            ball.vel_x = ball.speed * offset

        # Ball collision with bricks
        brick_hit = None
        for brick in bricks:
            if ball.get_rect().colliderect(brick.rect):
                brick_hit = brick
                break
        if brick_hit:
            bricks.remove(brick_hit)
            ball.vel_y = -ball.vel_y

        # Check game over conditions
        if ball.y - ball.radius > HEIGHT:
            game_over = True
        if not bricks:
            game_over = True

        # Drawing
        screen.fill(BLACK)
        for brick in bricks:
            brick.draw(screen)
        paddle.draw(screen)
        ball.draw(screen)

        if game_over:
            font = pygame.font.SysFont(None, 74)
            text = font.render("Game Over" if bricks else "You Win!", True, WHITE)
            screen.blit(text, (WIDTH // 2 - text.get_width() // 2,
                             HEIGHT // 2 - text.get_height() // 2))
            pygame.display.flip()
            pygame.time.delay(2000)
            running = False
            return

        pygame.display.flip() 