#!/usr/bin/env python3
import pygame
import pygame_menu
import random

# Constants
WIDTH, HEIGHT = 800, 600
FPS = 60

# Colours
BLACK  = (0, 0, 0)
WHITE  = (255, 255, 255)
RED    = (255, 0, 0)
GREEN  = (0, 255, 0)
BLUE   = (0, 0, 255)
YELLOW = (255, 255, 0)

# Initialize font
pygame.font.init()
FONT_SMALL = pygame.font.SysFont(None, 30)

class Paddle:
    def __init__(self, x, y, width, height, speed):
        self.rect = pygame.Rect(x, y, width, height)
        self.speed = speed

    def update(self, keys):
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
        # Clamp within screen bounds
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH

    def draw(self, screen):
        pygame.draw.rect(screen, WHITE, self.rect)

class Ball:
    def __init__(self, x, y, radius, speed):
        self.x = x
        self.y = y
        self.radius = radius
        self.speed = speed
        self.vel_x = random.choice([-1, 1]) * speed
        self.vel_y = -speed

    def update(self):
        self.x += self.vel_x
        self.y += self.vel_y
        # Bounce off left/right walls
        if self.x - self.radius <= 0 or self.x + self.radius >= WIDTH:
            self.vel_x = -self.vel_x
        # Bounce off top wall
        if self.y - self.radius <= 0:
            self.vel_y = -self.vel_y

    def draw(self, screen):
        pygame.draw.circle(screen, YELLOW, (int(self.x), int(self.y)), self.radius)

    def get_rect(self):
        return pygame.Rect(self.x - self.radius, self.y - self.radius,
                           self.radius * 2, self.radius * 2)

class Brick:
    def __init__(self, x, y, width, height, color):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)

def pause_menu(screen):
    # Using a mutable list to capture the resume/quit choice.
    resume = [True]

    def resume_game():
        resume[0] = True
        menu.disable()

    def quit_to_menu():
        resume[0] = False
        menu.disable()

    menu = pygame_menu.Menu('Paused', WIDTH, HEIGHT, theme=pygame_menu.themes.THEME_DARK)
    menu.add.button('Resume', resume_game)
    menu.add.button('Quit to Main Menu', quit_to_menu)
    menu.mainloop(screen)
    return resume[0]

def game_loop(screen):
    clock = pygame.time.Clock()
    paddle_width = 100
    paddle_height = 10
    paddle = Paddle(WIDTH // 2 - paddle_width // 2, HEIGHT - 30, paddle_width, paddle_height, 7)
    ball = Ball(WIDTH // 2, HEIGHT - 50, 8, 5)
    
    # Add game state variables
    score = 0
    lives = 3
    level = 1
    
    bricks = []
    rows = 5
    cols = 10
    spacing = 5
    brick_width = (WIDTH - (cols + 1) * spacing) / cols
    brick_height = 20

    # Create bricks arranged in rows and columns.
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
                    # Pause menu; if the player chooses to quit, return to main menu.
                    if not pause_menu(screen):
                        running = False
                        return

        if not game_over:
            keys = pygame.key.get_pressed()
            paddle.update(keys)
            ball.update()

            # Ball collision with paddle
            if ball.get_rect().colliderect(paddle.rect):
                ball.vel_y = -abs(ball.vel_y)
                # Adjust horizontal velocity based on hit position
                offset = (ball.x - paddle.rect.centerx) / (paddle.rect.width / 2)
                ball.vel_x = offset * ball.speed

            # Check for ball falling below screen
            if ball.y - ball.radius > HEIGHT:
                lives -= 1
                if lives > 0:
                    # Reset ball and paddle
                    paddle.rect.x = WIDTH // 2 - paddle_width // 2
                    ball.x, ball.y = WIDTH // 2, HEIGHT - 50
                    ball.vel_x = random.choice([-1, 1]) * ball.speed
                    ball.vel_y = -ball.speed
                else:
                    game_over = True
                    # Save score
                    with open("highscores.txt", "a") as f:
                        f.write(f"Score: {score} | Level: {level}\n")

            # Check brick collisions
            brick_hit = None
            for brick in bricks:
                if ball.get_rect().colliderect(brick.rect):
                    brick_hit = brick
                    ball.vel_y = -ball.vel_y
                    score += 10
                    break
            
            if brick_hit:
                bricks.remove(brick_hit)

            # Check for level completion
            if not bricks:
                level += 1
                # Increase ball speed slightly with each level
                ball.speed += 0.5
                # Reset positions
                paddle.rect.x = WIDTH // 2 - paddle_width // 2
                ball.x, ball.y = WIDTH // 2, HEIGHT - 50
                ball.vel_x = random.choice([-1, 1]) * ball.speed
                ball.vel_y = -ball.speed
                # Recreate bricks
                bricks.clear()
                for row in range(rows):
                    for col in range(cols):
                        x = spacing + col * (brick_width + spacing)
                        y = 50 + row * (brick_height + spacing)
                        color = random.choice([RED, GREEN, BLUE])
                        bricks.append(Brick(x, y, brick_width, brick_height, color))

        # Drawing section
        screen.fill(BLACK)
        paddle.draw(screen)
        ball.draw(screen)
        for brick in bricks:
            brick.draw(screen)

        # Draw HUD
        score_text = FONT_SMALL.render(f"Score: {score}", True, WHITE)
        lives_text = FONT_SMALL.render(f"Lives: {lives}", True, WHITE)
        level_text = FONT_SMALL.render(f"Level: {level}", True, WHITE)
        
        screen.blit(score_text, (10, 10))
        screen.blit(lives_text, (WIDTH - lives_text.get_width() - 10, 10))
        screen.blit(level_text, (WIDTH // 2 - level_text.get_width() // 2, 10))

        if game_over:
            game_over_text = FONT_SMALL.render("GAME OVER - Press ESC", True, RED)
            screen.blit(game_over_text, 
                       (WIDTH // 2 - game_over_text.get_width() // 2, 
                        HEIGHT // 2 - game_over_text.get_height() // 2))

        pygame.display.flip()

def main_menu():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Loftwahnoid")
    menu = pygame_menu.Menu('Loftwahnoid', WIDTH, HEIGHT, theme=pygame_menu.themes.THEME_DARK)
    menu.add.button('Play', lambda: game_loop(screen))
    menu.add.button('Quit', pygame_menu.events.EXIT)
    menu.mainloop(screen)

if __name__ == '__main__':
    main_menu()
