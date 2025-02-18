import pygame
from ..constants import WIDTH, HEIGHT, WHITE, GREEN, RED, BLUE, YELLOW

class PowerUp:
    # Define power-up types as class constants
    WIDE_PADDLE = "wide_paddle"
    EXTRA_LIFE = "extra_life"
    STICKY_PADDLE = "sticky_paddle"
    SHOOTING_PADDLE = "shooting_paddle"
    
    def __init__(self, x, y, power_type):
        self.x = x
        self.y = y
        self.power_type = power_type
        self.width = 20
        self.height = 20
        self.speed = 3
        self.rect = pygame.Rect(self.x - self.width // 2, self.y - self.height // 2, 
                              self.width, self.height)
        
        # Set color based on power-up type
        self.colors = {
            self.WIDE_PADDLE: GREEN,
            self.EXTRA_LIFE: RED,
            self.STICKY_PADDLE: BLUE,
            self.SHOOTING_PADDLE: YELLOW
        }
        self.color = self.colors.get(power_type, WHITE)

    def update(self):
        self.y += self.speed
        self.rect.y = self.y - self.height // 2

    def draw(self, screen):
        # Add pulsing effect
        current_time = pygame.time.get_ticks()
        scale = 1.0 + 0.1 * (current_time % 1000) / 1000  # Pulse between 1.0 and 1.1
        scaled_width = int(self.width * scale)
        scaled_height = int(self.height * scale)
        scaled_rect = pygame.Rect(
            self.x - scaled_width // 2,
            self.y - scaled_height // 2,
            scaled_width,
            scaled_height
        )
        
        # Draw glowing outline
        pygame.draw.rect(screen, WHITE, scaled_rect, 2)
        pygame.draw.rect(screen, self.color, self.rect)
        
        # Enhanced icons with "Loftwahnoid" branding
        font = pygame.font.SysFont(None, 12)
        if self.power_type == self.WIDE_PADDLE:
            pygame.draw.line(screen, WHITE, 
                            (self.rect.left + 4, self.rect.centery),
                            (self.rect.right - 4, self.rect.centery), 2)
            text = font.render("L", True, WHITE)
            screen.blit(text, (self.rect.centerx - 3, self.rect.centery - 5))
        elif self.power_type == self.EXTRA_LIFE:
            pygame.draw.line(screen, WHITE,
                            (self.rect.centerx, self.rect.top + 4),
                            (self.rect.centerx, self.rect.bottom - 4), 2)
            pygame.draw.line(screen, WHITE,
                            (self.rect.left + 4, self.rect.centery),
                            (self.rect.right - 4, self.rect.centery), 2)
            text = font.render("L", True, WHITE)
            screen.blit(text, (self.rect.centerx - 3, self.rect.centery - 5))
        elif self.power_type == self.STICKY_PADDLE:
            for x in range(self.rect.left + 5, self.rect.right - 2, 5):
                pygame.draw.circle(screen, WHITE, (x, self.rect.centery), 2)
            text = font.render("L", True, WHITE)
            screen.blit(text, (self.rect.centerx - 3, self.rect.centery - 5))
        elif self.power_type == self.SHOOTING_PADDLE:
            points = [
                (self.rect.centerx, self.rect.top + 4),
                (self.rect.centerx - 4, self.rect.centery),
                (self.rect.centerx + 4, self.rect.centery)
            ]
            pygame.draw.polygon(screen, WHITE, points)
            text = font.render("L", True, WHITE)
            screen.blit(text, (self.rect.centerx - 3, self.rect.bottom - 10))

    def apply_effect(self, paddle, lives):
        if self.power_type in [self.WIDE_PADDLE, self.STICKY_PADDLE, self.SHOOTING_PADDLE]:
            paddle.reset_width()
        
        if self.power_type == self.WIDE_PADDLE:
            paddle.rect.width = min(paddle.rect.width + 75, 250)  # Increased from 50->75, 200->250
        elif self.power_type == self.EXTRA_LIFE:
            lives += 2  # Give 2 lives instead of 1
        elif self.power_type == self.STICKY_PADDLE:
            paddle.sticky = True
            paddle.sticky_timer = pygame.time.get_ticks()
            paddle.sticky_duration = 15000  # Increased to 15s
        elif self.power_type == self.SHOOTING_PADDLE:
            paddle.shooting = True
            paddle.shoot_timer = pygame.time.get_ticks()
            paddle.shoot_cooldown = 500  # Faster shooting (was 750)
        return lives 