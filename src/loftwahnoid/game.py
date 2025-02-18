import pygame
import random
import os
from .constants import WIDTH, HEIGHT, FPS, BLACK, WHITE, RED, GREEN, BLUE
from .sprites.paddle import Paddle
from .sprites.ball import Ball
from .sprites.brick import Brick
from .pause import pause_menu
from .highscores import HighScoreManager
import pygame_menu

def game_loop(screen):
    # Initialize mixer and load sounds
    pygame.mixer.init()
    
    # Get the directory where the sounds are stored
    sound_dir = os.path.join(os.path.dirname(__file__), 'sounds')
    
    # Initialize with empty sounds in case files are missing
    sounds = {
        'music': None,
        'ding': None,
        'death': None,
        'life': None
    }
    
    # Try to load sounds if they exist
    try:
        sounds = {
            'music': pygame.mixer.Sound(os.path.join(sound_dir, 'music.wav')),
            'ding': pygame.mixer.Sound(os.path.join(sound_dir, 'ding.wav')),
            'death': pygame.mixer.Sound(os.path.join(sound_dir, 'death.wav')),
            'life': pygame.mixer.Sound(os.path.join(sound_dir, 'life.wav'))
        }
    except:
        print("Warning: Some sound files could not be loaded")

    clock = pygame.time.Clock()
    paddle_width = 100
    paddle_height = 10
    paddle = Paddle(WIDTH // 2 - paddle_width // 2, HEIGHT - 30, paddle_width, paddle_height, 7)
    ball = Ball(WIDTH // 2, HEIGHT - 50, 8, 5)
    ball.started = False  # Ball starts inactive
    
    # Game state variables
    score = 0
    lives = 3
    level = 1
    
    high_scores = HighScoreManager()

    # Play music at start
    if sounds['music']:
        sounds['music'].play()

    def generate_level(level):
        bricks = []
        rows = 5  # Back to fixed 5 rows
        cols = 10
        spacing = 5
        brick_width = (WIDTH - (cols + 1) * spacing) / cols
        brick_height = 20

        # Increase chance of tough bricks with level
        tough_brick_chance = min(0.1 + (level * 0.05), 0.4)  # Max 40% chance
        
        for row in range(rows):
            for col in range(cols):
                x = spacing + col * (brick_width + spacing)
                y = 50 + row * (brick_height + spacing)
                
                # Make top row always tough bricks
                if row == 0:
                    brick_type = Brick.TOUGH
                # Random tough bricks for other rows based on level
                elif random.random() < tough_brick_chance:
                    brick_type = Brick.TOUGH
                else:
                    brick_type = Brick.NORMAL
                    
                bricks.append(Brick(x, y, brick_width, brick_height, brick_type))
        
        return bricks

    # Initial brick creation
    bricks = generate_level(level)

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
                elif event.key == pygame.K_SPACE and not ball.started:
                    ball.start()  # Initialize velocities when starting

        keys = pygame.key.get_pressed()
        paddle.update(keys)

        # Update ball position
        if not game_over:
            if ball.started:
                ball.update()
            else:
                # Keep ball on paddle until space is pressed
                ball.x = paddle.rect.centerx
                ball.y = paddle.rect.top - ball.radius

        # Only check collisions if ball is in motion
        if ball.started:
            # Ball collision with paddle
            if ball.get_rect().colliderect(paddle.rect):
                ball.vel_y = -abs(ball.vel_y)  # Ensure ball goes upward
                offset = (ball.x - paddle.rect.centerx) / (paddle.rect.width / 2)
                ball.vel_x = ball.speed * offset

            # Ball collision with bricks
            brick_hit = None
            for brick in bricks:
                if ball.get_rect().colliderect(brick.rect):
                    brick_hit = brick
                    break
                    
            if brick_hit:
                if brick_hit.hit():
                    bricks.remove(brick_hit)
                    score += 20 if brick_hit.brick_type == Brick.TOUGH else 10
                ball.vel_y = -ball.vel_y  # Make sure ball bounces
                if sounds['ding']:
                    sounds['ding'].play()

        # Check game over conditions
        if ball.y - ball.radius > HEIGHT:
            lives -= 1
            if sounds['death']:
                sounds['death'].play()
            if lives <= 0:
                game_over = True
            else:
                # Reset ball position and state
                ball.x = paddle.rect.centerx
                ball.y = paddle.rect.top - ball.radius
                ball.started = False
                ball.vel_x = 0  # Reset velocity
                ball.vel_y = 0  # Reset velocity
                
        # Level complete
        if not bricks:
            level += 1
            # Reset ball position and state
            ball.x = paddle.rect.centerx
            ball.y = paddle.rect.top - ball.radius
            ball.started = False
            ball.vel_x = 0
            ball.vel_y = 0
            
            # Generate new level
            bricks = generate_level(level)
            
            if sounds['music']:
                sounds['music'].play()

        # Drawing
        screen.fill(BLACK)
        for brick in bricks:
            brick.draw(screen)
        paddle.draw(screen)
        ball.draw(screen)

        # Draw score, lives and level with better layout
        font = pygame.font.SysFont(None, 36)
        
        # Left align score
        score_text = font.render(f'Score: {score}', True, WHITE)
        screen.blit(score_text, (20, 20))
        
        # Center align lives
        lives_text = font.render(f'Lives: {lives}', True, WHITE)
        lives_x = WIDTH // 2 - lives_text.get_width() // 2
        screen.blit(lives_text, (lives_x, 20))
        
        # Right align level
        level_text = font.render(f'Level: {level}', True, WHITE)
        level_x = WIDTH - level_text.get_width() - 20
        screen.blit(level_text, (level_x, 20))

        if game_over:
            # Get player name
            name = pygame_menu.widgets.TextInput(
                'Enter your name: ',
                maxchar=10,
                textinput_id='name_input'
            )
            menu = pygame_menu.Menu(
                'Game Over',
                WIDTH, HEIGHT,
                theme=pygame_menu.themes.THEME_DARK
            )
            menu.add.generic_widget(name)
            menu.add.button('Submit', lambda: high_scores.add_score(name.get_value(), score, level))
            menu.add.button('Quit', pygame_menu.events.EXIT)
            menu.mainloop(screen)
            return

        pygame.display.flip() 