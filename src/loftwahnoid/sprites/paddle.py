import pygame
from ..constants import WIDTH, WHITE, YELLOW

class Paddle:
    def __init__(self, x, y, width, height, speed):
        self.rect = pygame.Rect(x, y, width, height)
        self.original_width = width
        self.speed = speed
        self.sticky = False
        self.sticky_timer = 0
        self.sticky_duration = 10000  # 10 seconds
        self.shooting = False
        self.shoot_timer = 0
        self.shoot_cooldown = 750  # Increased from 500 to 750ms
        self.last_shot = 0
        self.bullets = []
        
    def update(self, keys):
        current_time = pygame.time.get_ticks()
        
        # Movement
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
            
        # Clamp within screen bounds
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
            
        # Check sticky timer
        if self.sticky and current_time - self.sticky_timer > self.sticky_duration:
            self.sticky = False
            
        # Check shooting timer
        if self.shooting and current_time - self.shoot_timer > 7000:  # 7 seconds
            self.shooting = False
            self.bullets.clear()
            
        # Handle shooting
        if self.shooting and keys[pygame.K_SPACE]:
            if current_time - self.last_shot > self.shoot_cooldown and len(self.bullets) < 3:
                self.bullets.append(Bullet(self.rect.centerx, self.rect.top))
                self.last_shot = current_time
                
        # Update bullets
        for bullet in self.bullets[:]:
            bullet.update()
            if bullet.rect.bottom < 0:  # Remove if off screen
                self.bullets.remove(bullet)

    def draw(self, screen):
        pygame.draw.rect(screen, WHITE, self.rect)
        if self.sticky:
            # Draw sticky indicator dots
            for x in range(self.rect.left + 10, self.rect.right - 5, 10):
                pygame.draw.circle(screen, YELLOW, (x, self.rect.top + 2), 2)
        if self.shooting:
            # Draw shooting indicator triangles
            pygame.draw.polygon(screen, YELLOW, [
                (self.rect.left + 5, self.rect.top + 5),
                (self.rect.left + 10, self.rect.top),
                (self.rect.left + 15, self.rect.top + 5)
            ])
            pygame.draw.polygon(screen, YELLOW, [
                (self.rect.right - 15, self.rect.top + 5),
                (self.rect.right - 10, self.rect.top),
                (self.rect.right - 5, self.rect.top + 5)
            ])
        # Draw bullets
        for bullet in self.bullets:
            bullet.draw(screen)

    def reset_width(self):
        self.rect.width = self.original_width
        self.sticky = False
        self.shooting = False
        self.bullets.clear()

class Bullet:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x - 2, y - 8, 4, 8)
        self.speed = 8

    def update(self):
        self.rect.y -= self.speed

    def draw(self, screen):
        pygame.draw.rect(screen, YELLOW, self.rect) 