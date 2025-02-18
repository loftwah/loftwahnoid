import pygame
from ..constants import WIDTH, HEIGHT, WHITE, GREEN, RED, BLUE, YELLOW
import random

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
        self.particles = []
        self.last_particle_time = pygame.time.get_ticks()

    def update(self):
        self.y += self.speed
        self.rect.y = self.y - self.height // 2
        current_time = pygame.time.get_ticks()
        if current_time - self.last_particle_time > 100:
            self.particles.append({
                'x': self.x + random.randint(-5, 5),
                'y': self.y - self.height // 2,
                'life': 30,
                'color': self.color
            })
            self.last_particle_time = current_time
        for particle in self.particles[:]:
            particle['y'] -= 1
            particle['life'] -= 1
            if particle['life'] <= 0:
                self.particles.remove(particle)

    def draw(self, screen):
        current_time = pygame.time.get_ticks()
        scale = 1.0 + 0.3 * abs((current_time % 1000) / 500 - 1)
        scaled_width = int(self.width * scale)
        scaled_height = int(self.height * scale)
        scaled_rect = pygame.Rect(
            self.x - scaled_width // 2,
            self.y - scaled_height // 2,
            scaled_width,
            scaled_height
        )
        for particle in self.particles:
            alpha = int(255 * (particle['life'] / 30))
            particle_color = (*self.color[:3], alpha)
            surface = pygame.Surface((4, 4), pygame.SRCALPHA)
            pygame.draw.circle(surface, particle_color, (2, 2), 2)
            screen.blit(surface, (int(particle['x']), int(particle['y'])))
        outline_surface = pygame.Surface((scaled_width + 4, scaled_height + 4), pygame.SRCALPHA)
        pygame.draw.rect(outline_surface, (*WHITE[:3], 100), (2, 2, scaled_width, scaled_height), 2)
        screen.blit(outline_surface, (self.x - scaled_width // 2 - 2, self.y - scaled_height // 2 - 2))
        pygame.draw.rect(screen, self.color, scaled_rect)
        font = pygame.font.SysFont(None, 12)
        if self.power_type == self.WIDE_PADDLE:
            pygame.draw.line(screen, WHITE, 
                            (scaled_rect.left + 4, scaled_rect.centery),
                            (scaled_rect.right - 4, scaled_rect.centery), 2)
            text = font.render("L", True, WHITE)
            screen.blit(text, (scaled_rect.centerx - 3, scaled_rect.centery - 5))
        elif self.power_type == self.EXTRA_LIFE:
            pygame.draw.line(screen, WHITE,
                            (scaled_rect.centerx, scaled_rect.top + 4),
                            (scaled_rect.centerx, scaled_rect.bottom - 4), 2)
            pygame.draw.line(screen, WHITE,
                            (scaled_rect.left + 4, scaled_rect.centery),
                            (scaled_rect.right - 4, scaled_rect.centery), 2)
            text = font.render("L", True, WHITE)
            screen.blit(text, (scaled_rect.centerx - 3, scaled_rect.centery - 5))
        elif self.power_type == self.STICKY_PADDLE:
            for x in range(scaled_rect.left + 5, scaled_rect.right - 2, 5):
                pygame.draw.circle(screen, WHITE, (x, scaled_rect.centery), 2)
            text = font.render("L", True, WHITE)
            screen.blit(text, (scaled_rect.centerx - 3, scaled_rect.centery - 5))
        elif self.power_type == self.SHOOTING_PADDLE:
            points = [
                (scaled_rect.centerx, scaled_rect.top + 4),
                (scaled_rect.centerx - 4, scaled_rect.centery),
                (scaled_rect.centerx + 4, scaled_rect.centery)
            ]
            pygame.draw.polygon(screen, WHITE, points)
            text = font.render("L", True, WHITE)
            screen.blit(text, (scaled_rect.centerx - 3, scaled_rect.bottom - 10))

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