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
        # Draw power-up with a distinctive shape for each type
        pygame.draw.rect(screen, self.color, self.rect)
        
        # Draw an icon inside based on power-up type
        if self.power_type == self.WIDE_PADDLE:
            # Draw horizontal line
            pygame.draw.line(screen, WHITE, 
                           (self.rect.left + 4, self.rect.centery),
                           (self.rect.right - 4, self.rect.centery), 2)
        elif self.power_type == self.EXTRA_LIFE:
            # Draw a plus symbol
            pygame.draw.line(screen, WHITE,
                           (self.rect.centerx, self.rect.top + 4),
                           (self.rect.centerx, self.rect.bottom - 4), 2)
            pygame.draw.line(screen, WHITE,
                           (self.rect.left + 4, self.rect.centery),
                           (self.rect.right - 4, self.rect.centery), 2)
        elif self.power_type == self.STICKY_PADDLE:
            # Draw dots pattern
            for x in range(self.rect.left + 5, self.rect.right - 2, 5):
                pygame.draw.circle(screen, WHITE, (x, self.rect.centery), 1)
        elif self.power_type == self.SHOOTING_PADDLE:
            # Draw arrow up symbol
            points = [
                (self.rect.centerx, self.rect.top + 4),
                (self.rect.centerx - 4, self.rect.centery),
                (self.rect.centerx + 4, self.rect.centery)
            ]
            pygame.draw.polygon(screen, WHITE, points)

    def apply_effect(self, paddle, lives):
        # Reset all paddle-altering states first if it's a paddle power-up
        if self.power_type in [self.WIDE_PADDLE, self.STICKY_PADDLE, self.SHOOTING_PADDLE]:
            paddle.reset_width()  # Resets width, sticky, shooting, and bullets
        
        if self.power_type == self.WIDE_PADDLE:
            paddle.rect.width = min(paddle.rect.width + 50, 200)
        elif self.power_type == self.EXTRA_LIFE:
            lives += 1
        elif self.power_type == self.STICKY_PADDLE:
            paddle.sticky = True
            paddle.sticky_timer = pygame.time.get_ticks()
        elif self.power_type == self.SHOOTING_PADDLE:
            paddle.shooting = True
            paddle.shoot_timer = pygame.time.get_ticks()
        return lives 