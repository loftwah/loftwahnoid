import pygame
import random
import os
from .constants import WIDTH, HEIGHT, FPS, BLACK, WHITE, RED, GREEN, BLUE, YELLOW
from .sprites.paddle import Paddle
from .sprites.ball import Ball
from .sprites.brick import Brick
from .pause import pause_menu
from .highscores import HighScoreManager
import pygame_menu
from .sprites.powerup import PowerUp

def game_loop(screen):
    # Initialize mixer and load sounds
    pygame.mixer.init()
    pygame.font.init()  # Add this line to initialize font system
    
    # Get the directory where the sounds are stored
    sound_dir = os.path.join(os.path.dirname(__file__), 'sounds')
    
    # Initialize fonts after pygame.font.init()
    font = pygame.font.SysFont(None, 36)
    
    # Initialize with empty sounds in case files are missing
    sounds = {
        'music': None,
        'ding': None,
        'death': None,
        'life': None,
        'powerup': None
    }
    
    # Try to load sounds if they exist
    try:
        sounds = {
            'music': pygame.mixer.Sound(os.path.join(sound_dir, 'music.wav')),
            'ding': pygame.mixer.Sound(os.path.join(sound_dir, 'ding.wav')),
            'death': pygame.mixer.Sound(os.path.join(sound_dir, 'death.wav')),
            'life': pygame.mixer.Sound(os.path.join(sound_dir, 'life.wav')),
            'powerup': pygame.mixer.Sound(os.path.join(sound_dir, 'powerup.wav'))
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

    # Add near the top of game_loop, after sounds initialization
    # Power-up spawn rates (40% total chance of any power-up spawning per brick)
    POWERUP_SPAWN_RATES = {
        PowerUp.WIDE_PADDLE: 0.15,      # 15% chance
        PowerUp.EXTRA_LIFE: 0.05,       # 5% chance (rarer)
        PowerUp.STICKY_PADDLE: 0.10,    # 10% chance
        PowerUp.SHOOTING_PADDLE: 0.10   # 10% chance
    }

    # Add after bricks/power_ups initialization
    sticky_just_activated = False
    paddle_flash_timer = None

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
    power_ups = []  # Add this line to store active power-ups

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
                elif event.key == pygame.K_SPACE:
                    if not ball.started:
                        ball.start()  # Initialize velocities when starting
                    elif paddle.sticky and ball.stuck_to_paddle:
                        # Release ball from sticky paddle
                        ball.started = True
                        ball.stuck_to_paddle = False
                        ball.vel_y = -abs(ball.vel_y)  # Ensure ball goes upward
                        offset = (ball.x - paddle.rect.centerx) / (paddle.rect.width / 2)
                        ball.vel_x = ball.speed * offset

        keys = pygame.key.get_pressed()
        paddle.update(keys)

        # Update the ball position and powerups section to separate their updates
        if not game_over:
            # Always update power-ups regardless of ball state
            for power_up in power_ups[:]:  # Use slice to safely remove while iterating
                power_up.update()
                # Remove if fallen off screen
                if power_up.y > HEIGHT:
                    power_ups.remove(power_up)
                # Check collision with paddle
                elif paddle.rect.colliderect(power_up.rect):
                    old_sticky = paddle.sticky
                    lives = power_up.apply_effect(paddle, lives)
                    if power_up.power_type == PowerUp.EXTRA_LIFE and sounds['life']:
                        sounds['life'].play()  # Add distinct sound for extra life
                    elif sounds['powerup']:
                        sounds['powerup'].play()
                    power_ups.remove(power_up)
            
            # Update ball position separately
            if ball.started:
                ball.update()
            else:
                # Keep ball on paddle until space is pressed
                ball.x = paddle.rect.centerx
                ball.y = paddle.rect.top - ball.radius

        # Check if ball should be released when sticky expires
        if not game_over and ball.stuck_to_paddle and not paddle.sticky:
            ball.start()  # Release ball with initial velocity

        # Only check collisions if ball is in motion
        if ball.started:
            # Ball collision with paddle
            if ball.get_rect().colliderect(paddle.rect):
                if paddle.sticky:
                    if not ball.stuck_to_paddle:
                        # Stick ball where it hits
                        ball.stuck_to_paddle = True
                        ball.started = False
                        ball.vel_x = 0
                        ball.vel_y = 0
                        ball.y = paddle.rect.top - ball.radius - 2
                        # ball.x remains where it landed
                else:
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
                if brick_hit.hit():
                    bricks.remove(brick_hit)
                    score += 20 if brick_hit.brick_type == Brick.TOUGH else 10
                    
                    # Roll for powerup spawn
                    if random.random() < sum(POWERUP_SPAWN_RATES.values()):
                        power_type = random.choices(
                            list(POWERUP_SPAWN_RATES.keys()),
                            weights=list(POWERUP_SPAWN_RATES.values()),
                            k=1
                        )[0]
                        spawn_x = max(20, min(brick_hit.rect.centerx, WIDTH - 20))
                        power_up = PowerUp(spawn_x, brick_hit.rect.centery, power_type)
                        power_ups.append(power_up)
                        
                ball.vel_y = -ball.vel_y
                if sounds['ding']:
                    sounds['ding'].play()

            # Check bullet collisions with bricks
            for bullet in paddle.bullets[:]:
                brick_hit = None
                for brick in bricks:
                    if bullet.rect.colliderect(brick.rect):
                        brick_hit = brick
                        break
                if brick_hit:
                    if brick_hit.hit():
                        bricks.remove(brick_hit)
                        score += 20 if brick_hit.brick_type == Brick.TOUGH else 10
                    paddle.bullets.remove(bullet)
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
                ball.vel_x = 0
                ball.vel_y = 0
                paddle.rect.width = 100  # Reset paddle width to normal
                
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
        for power_up in power_ups:
            power_up.draw(screen)

        # Draw score, lives and level with better layout
        score_text = font.render(f'Score: {score}', True, WHITE)
        screen.blit(score_text, (20, 20))  # Back to original y=20
        
        # Center align lives
        lives_text = font.render(f'Lives: {lives}', True, WHITE)
        lives_x = WIDTH // 2 - lives_text.get_width() // 2
        screen.blit(lives_text, (lives_x, 20))  # Back to original y=20
        
        # Right align level
        level_text = font.render(f'Level: {level}', True, WHITE)
        level_x = WIDTH - level_text.get_width() - 20
        screen.blit(level_text, (level_x, 20))  # Back to original y=20

        # Update paddle drawing to handle flashing
        current_time = pygame.time.get_ticks()
        if paddle_flash_timer and current_time - paddle_flash_timer < 500:  # Flash for 0.5 seconds
            if (current_time // 100) % 2 == 0:
                pygame.draw.rect(screen, YELLOW, paddle.rect)
            else:
                paddle.draw(screen)
        else:
            paddle.draw(screen)

        # Draw power-up status below lives
        draw_powerup_status(screen, paddle, font)

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

def draw_powerup_status(screen, paddle, font):
    active_powers = []
    current_time = pygame.time.get_ticks()
    
    if paddle.sticky:
        time_left = (paddle.sticky_duration - (current_time - paddle.sticky_timer)) // 1000
        active_powers.append(f"Sticky: {max(0, time_left)}s")
    if paddle.shooting:
        time_left = (7000 - (current_time - paddle.shoot_timer)) // 1000  # 7s duration
        active_powers.append(f"Shooting: {max(0, time_left)}s")
    if paddle.rect.width > paddle.original_width:
        active_powers.append("Wide Paddle")
    
    # Draw power-up status below lives (back to original y=60)
    for i, power in enumerate(active_powers):
        power_text = font.render(power, True, YELLOW)
        power_x = WIDTH // 2 - power_text.get_width() // 2
        screen.blit(power_text, (power_x, 60 + i * 30))  # Back to original y=60 